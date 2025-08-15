import openai
from typing import List, Dict, Optional
import logging
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

try:
    from models.cloud_vector_store import CloudVectorStoreManager as VectorStoreManager
except ImportError:
    from models.vector_store import VectorStoreManager

from config.settings import settings

logger = logging.getLogger(__name__)

class RAGQueryEngine:
    def __init__(self, use_local_embeddings: bool = True):
        """
        Initialize RAG query engine
        
        Args:
            use_local_embeddings: Whether to use local embeddings for vector search
        """
        self.vector_store = VectorStoreManager(use_local_embeddings)
        openai.api_key = settings.openai_api_key
        
        # System prompt for nutrition bot
        self.system_prompt = """You are a professional nutrition tutor bot with expertise in dietetics, sports nutrition, and meal planning. Your role is to provide evidence-based, personalized nutrition guidance.

INSTRUCTIONS:
- Always base your responses on the provided context from the nutrition database
- Provide specific, actionable advice
- Include relevant nutritional data when available
- Acknowledge limitations and recommend consulting healthcare professionals for medical concerns
- Be encouraging and supportive while remaining scientifically accurate
- Use clear, accessible language

RESPONSE STRUCTURE:
1. Direct answer to the user's question
2. Relevant nutritional information and data
3. Practical recommendations or next steps
4. Any important disclaimers or considerations

Remember: You complement but do not replace professional medical advice."""
    
    def generate_response(
        self,
        query: str,
        user_context: Optional[Dict] = None,
        response_style: str = "comprehensive"
    ) -> Dict:
        """
        Generate response using RAG approach
        
        Args:
            query: User's question
            user_context: Optional user information (age, goals, preferences, etc.)
            response_style: "brief", "comprehensive", or "detailed"
        
        Returns:
            Dict with response, sources, and metadata
        """
        try:
            # Step 1: Analyze query to determine search strategy
            search_strategy = self._analyze_query(query)
            
            # Step 2: Retrieve relevant context
            context_docs = self._retrieve_context(query, search_strategy)
            
            # Step 3: Generate response using LLM
            response = self._generate_llm_response(
                query, 
                context_docs, 
                user_context,
                response_style
            )
            
            return {
                "response": response,
                "sources": [doc["metadata"] for doc in context_docs],
                "search_strategy": search_strategy,
                "context_count": len(context_docs)
            }
            
        except Exception as e:
            logger.error(f"Error generating RAG response: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your question. Please try rephrasing your query or contact support.",
                "sources": [],
                "error": str(e)
            }
    
    def _analyze_query(self, query: str) -> Dict:
        """Analyze query to determine optimal search strategy"""
        query_lower = query.lower()
        
        strategy = {
            "food_focus": False,
            "knowledge_focus": False,
            "recipe_focus": False,
            "meal_planning_focus": False,
            "sports_nutrition_focus": False
        }
        
        # Food-focused queries
        food_keywords = ["food", "eat", "nutrition facts", "calories in", "protein in", "vitamins in"]
        if any(keyword in query_lower for keyword in food_keywords):
            strategy["food_focus"] = True
        
        # Knowledge/guideline queries
        knowledge_keywords = ["how much", "daily requirement", "recommended", "guidelines", "should I"]
        if any(keyword in query_lower for keyword in knowledge_keywords):
            strategy["knowledge_focus"] = True
        
        # Recipe queries
        recipe_keywords = ["recipe", "meal ideas", "combine", "mix", "prepare"]
        if any(keyword in query_lower for keyword in recipe_keywords):
            strategy["recipe_focus"] = True
        
        # Meal planning queries
        meal_keywords = ["meal plan", "diet plan", "weekly", "daily meals", "menu"]
        if any(keyword in query_lower for keyword in meal_keywords):
            strategy["meal_planning_focus"] = True
        
        # Sports nutrition queries
        sports_keywords = ["workout", "exercise", "athletic", "performance", "recovery", "pre-workout", "post-workout"]
        if any(keyword in query_lower for keyword in sports_keywords):
            strategy["sports_nutrition_focus"] = True
        
        return strategy
    
    def _retrieve_context(self, query: str, strategy: Dict) -> List[Dict]:
        """Retrieve relevant context based on search strategy"""
        all_results = []
        
        # Base search
        base_results = self.vector_store.similarity_search(query, n_results=5)
        all_results.extend(base_results)
        
        # Focused searches based on strategy
        if strategy["food_focus"]:
            food_results = self.vector_store.hybrid_search(
                query, n_results=3, food_focus=True
            )
            all_results.extend(food_results)
        
        if strategy["knowledge_focus"]:
            knowledge_results = self.vector_store.hybrid_search(
                query, n_results=3, knowledge_focus=True
            )
            all_results.extend(knowledge_results)
        
        if strategy["sports_nutrition_focus"]:
            sports_results = self.vector_store.similarity_search(
                f"sports nutrition exercise {query}",
                n_results=2,
                filter_dict={"category": "Sports Nutrition"}
            )
            all_results.extend(sports_results)
        
        # Remove duplicates and keep top results
        seen_ids = set()
        unique_results = []
        for result in all_results:
            if result["id"] not in seen_ids and result["similarity"] > 0.3:
                unique_results.append(result)
                seen_ids.add(result["id"])
        
        # Sort by relevance and limit results
        unique_results.sort(key=lambda x: x["similarity"], reverse=True)
        return unique_results[:8]  # Limit context to avoid token limits
    
    def _generate_llm_response(
        self, 
        query: str, 
        context_docs: List[Dict],
        user_context: Optional[Dict],
        response_style: str
    ) -> str:
        """Generate response using OpenAI with retrieved context"""
        
        # Build context string
        context_str = self._build_context_string(context_docs)
        
        # Build user context string
        user_context_str = ""
        if user_context:
            user_context_str = f"\nUSER CONTEXT:\n{self._format_user_context(user_context)}\n"
        
        # Adjust prompt based on response style
        style_instructions = {
            "brief": "Provide a concise, direct answer in 2-3 sentences.",
            "comprehensive": "Provide a thorough but accessible explanation with practical recommendations.",
            "detailed": "Provide an in-depth response with detailed explanations, multiple options, and comprehensive guidance."
        }
        
        style_instruction = style_instructions.get(response_style, style_instructions["comprehensive"])
        
        # Create the full prompt
        user_prompt = f"""CONTEXT FROM NUTRITION DATABASE:
{context_str}
{user_context_str}
USER QUESTION: {query}

RESPONSE STYLE: {style_instruction}

Please provide a helpful, evidence-based response using the context provided above."""
        
        try:
            response = openai.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=settings.temperature
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error calling OpenAI API: {e}")
            return f"I apologize, but I'm currently unable to process your question due to a technical issue. Please try again in a moment."
    
    def _build_context_string(self, context_docs: List[Dict]) -> str:
        """Build formatted context string from retrieved documents"""
        context_parts = []
        
        for i, doc in enumerate(context_docs, 1):
            doc_type = doc["metadata"].get("doc_type", "unknown")
            
            if doc_type == "food_item":
                food_name = doc["metadata"].get("food_name", "Unknown Food")
                context_parts.append(f"{i}. FOOD: {food_name}\n   {doc['content']}\n")
            
            elif doc_type == "nutrition_knowledge":
                topic = doc["metadata"].get("topic", "Nutrition Info")
                context_parts.append(f"{i}. GUIDELINE: {topic}\n   {doc['content']}\n")
            
            elif doc_type == "recipe_combination":
                recipe_name = doc["metadata"].get("recipe_name", "Recipe")
                context_parts.append(f"{i}. RECIPE: {recipe_name}\n   {doc['content']}\n")
            
            else:
                context_parts.append(f"{i}. INFO: {doc['content']}\n")
        
        return "\n".join(context_parts)
    
    def _format_user_context(self, user_context: Dict) -> str:
        """Format user context information"""
        context_parts = []
        
        if "age" in user_context:
            context_parts.append(f"Age: {user_context['age']}")
        if "gender" in user_context:
            context_parts.append(f"Gender: {user_context['gender']}")
        if "activity_level" in user_context:
            context_parts.append(f"Activity Level: {user_context['activity_level']}")
        if "goals" in user_context:
            context_parts.append(f"Goals: {user_context['goals']}")
        if "dietary_restrictions" in user_context:
            context_parts.append(f"Dietary Restrictions: {user_context['dietary_restrictions']}")
        if "preferences" in user_context:
            context_parts.append(f"Food Preferences: {user_context['preferences']}")
        
        return " | ".join(context_parts)
    
    def get_food_recommendations(
        self, 
        goal: str, 
        preferences: List[str] = None,
        restrictions: List[str] = None
    ) -> Dict:
        """Get specific food recommendations based on goals and preferences"""
        
        # Build query based on parameters
        query = f"foods for {goal}"
        if preferences:
            query += f" preferences: {', '.join(preferences)}"
        if restrictions:
            query += f" avoiding: {', '.join(restrictions)}"
        
        # Focus search on food items
        results = self.vector_store.hybrid_search(
            query, 
            n_results=10, 
            food_focus=True
        )
        
        # Group by food category
        recommendations_by_category = {}
        for result in results:
            category = result["metadata"].get("category", "Other")
            if category not in recommendations_by_category:
                recommendations_by_category[category] = []
            
            food_info = {
                "name": result["metadata"].get("food_name", "Unknown"),
                "calories": result["metadata"].get("calories", 0),
                "protein": result["metadata"].get("protein", 0),
                "benefits": result["metadata"].get("health_benefits", ""),
                "relevance": result["similarity"]
            }
            recommendations_by_category[category].append(food_info)
        
        return {
            "goal": goal,
            "recommendations": recommendations_by_category,
            "total_foods": sum(len(foods) for foods in recommendations_by_category.values())
        }

def test_rag_engine():
    """Test the RAG engine functionality"""
    print("🧪 Testing RAG Engine...")
    
    # Initialize RAG engine
    rag = RAGQueryEngine(use_local_embeddings=True)
    
    # Test queries
    test_queries = [
        {
            "query": "What are the best high-protein foods for building muscle?",
            "user_context": {"age": 25, "gender": "male", "goals": "muscle building", "activity_level": "high"}
        },
        {
            "query": "I need foods high in vitamin C for my immune system",
            "user_context": {"preferences": ["fruits", "vegetables"]}
        },
        {
            "query": "Help me plan meals for weight loss",
            "user_context": {"goals": "weight loss", "dietary_restrictions": ["dairy-free"]}
        }
    ]
    
    for i, test in enumerate(test_queries, 1):
        print(f"\n🔍 Test {i}: {test['query']}")
        
        result = rag.generate_response(
            test["query"], 
            user_context=test.get("user_context"),
            response_style="comprehensive"
        )
        
        print(f"📊 Found {result['context_count']} relevant sources")
        print(f"🎯 Search strategy: {result['search_strategy']}")
        print(f"💬 Response: {result['response'][:200]}...")
        
        if result["sources"]:
            print("📚 Top sources:")
            for source in result["sources"][:2]:
                source_name = source.get("food_name", source.get("topic", "Unknown"))
                print(f"   - {source_name} ({source.get('doc_type', 'unknown')})")
    
    print("\n✅ RAG engine test completed!")

if __name__ == "__main__":
    test_rag_engine()