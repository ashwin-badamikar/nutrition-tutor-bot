"""
Enhanced RAG Engine with Conversational Memory
Extends the basic RAG engine to handle multi-turn conversations
"""

import openai
from typing import List, Dict, Optional
import logging
from models.vector_store import VectorStoreManager
from config.settings import settings

logger = logging.getLogger(__name__)

class ConversationalRAGEngine:
    def __init__(self, use_local_embeddings: bool = True):
        """
        Initialize conversational RAG engine with memory
        """
        self.vector_store = VectorStoreManager(use_local_embeddings)
        openai.api_key = settings.openai_api_key
        
        # Enhanced system prompt for conversational nutrition bot
        self.system_prompt = """You are a professional, conversational nutrition tutor bot with expertise in dietetics, sports nutrition, and meal planning. You maintain context across conversations and provide personalized, evidence-based guidance.

CONVERSATIONAL GUIDELINES:
- Remember and reference previous parts of our conversation
- Build on previous answers when relevant
- Ask clarifying questions when helpful
- Maintain a friendly, supportive, coaching tone
- Provide specific, actionable advice
- Always base responses on the provided nutrition database context

RESPONSE APPROACH:
- Acknowledge previous conversation when relevant
- Provide direct answers to questions
- Include relevant nutritional data and recommendations
- Suggest follow-up questions or next steps
- Be encouraging and motivating

Remember: You're a nutrition coach having an ongoing conversation, not just answering isolated questions."""
    
    def generate_conversational_response(
        self,
        current_query: str,
        conversation_history: List[Dict] = None,
        user_context: Optional[Dict] = None,
        response_style: str = "comprehensive"
    ) -> Dict:
        """
        Generate response with conversation memory
        
        Args:
            current_query: Current user question
            conversation_history: Previous chat messages
            user_context: User profile information
            response_style: Response length preference
        
        Returns:
            Dict with response, sources, and conversation metadata
        """
        try:
            # Step 1: Analyze current query with conversation context
            search_strategy = self._analyze_conversational_query(current_query, conversation_history)
            
            # Step 2: Retrieve relevant context (enhanced with conversation awareness)
            context_docs = self._retrieve_conversational_context(current_query, conversation_history, search_strategy)
            
            # Step 3: Generate contextual response
            response = self._generate_conversational_response(
                current_query,
                context_docs,
                conversation_history,
                user_context,
                response_style
            )
            
            return {
                "response": response,
                "sources": [doc["metadata"] for doc in context_docs],
                "search_strategy": search_strategy,
                "context_count": len(context_docs),
                "conversation_aware": True
            }
            
        except Exception as e:
            logger.error(f"Error in conversational RAG: {e}")
            return {
                "response": "I apologize, but I encountered an error processing your question. Could you please rephrase it or ask something else?",
                "sources": [],
                "error": str(e)
            }
    
    def _analyze_conversational_query(self, query: str, history: List[Dict] = None) -> Dict:
        """Analyze query with conversation context"""
        query_lower = query.lower()
        
        strategy = {
            "food_focus": False,
            "knowledge_focus": False,
            "recipe_focus": False,
            "meal_planning_focus": False,
            "sports_nutrition_focus": False,
            "follow_up_question": False,
            "clarification_request": False
        }
        
        # Check if this is a follow-up question
        follow_up_indicators = ["what about", "tell me more", "can you explain", "more details", "also", "additionally", "further"]
        if any(indicator in query_lower for indicator in follow_up_indicators):
            strategy["follow_up_question"] = True
        
        # Check if asking for clarification
        clarification_indicators = ["which", "how much", "how many", "when should", "can you be more specific"]
        if any(indicator in query_lower for indicator in clarification_indicators):
            strategy["clarification_request"] = True
        
        # Analyze conversation context if available
        if history and len(history) >= 2:
            recent_topics = []
            for msg in history[-4:]:  # Look at last 4 messages
                if msg['role'] == 'assistant':
                    content = msg['content'].lower()
                    if 'protein' in content: recent_topics.append('protein')
                    if 'weight' in content: recent_topics.append('weight_management')
                    if 'workout' in content or 'exercise' in content: recent_topics.append('sports_nutrition')
                    if 'meal' in content or 'breakfast' in content: recent_topics.append('meal_planning')
            
            # Enhance strategy based on conversation topics
            if 'protein' in recent_topics: strategy["food_focus"] = True
            if 'weight_management' in recent_topics: strategy["knowledge_focus"] = True
            if 'sports_nutrition' in recent_topics: strategy["sports_nutrition_focus"] = True
            if 'meal_planning' in recent_topics: strategy["meal_planning_focus"] = True
        
        # Apply standard query analysis
        food_keywords = ["food", "eat", "nutrition facts", "calories in", "protein in"]
        if any(keyword in query_lower for keyword in food_keywords):
            strategy["food_focus"] = True
        
        knowledge_keywords = ["how much", "daily requirement", "recommended", "should I"]
        if any(keyword in query_lower for keyword in knowledge_keywords):
            strategy["knowledge_focus"] = True
        
        return strategy
    
    def _retrieve_conversational_context(self, query: str, history: List[Dict], strategy: Dict) -> List[Dict]:
        """Retrieve context with conversation awareness"""
        
        # Build enhanced query with conversation context
        enhanced_query = query
        
        if history and strategy.get("follow_up_question"):
            # For follow-up questions, include recent conversation topics
            recent_assistant_responses = [
                msg['content'] for msg in history[-4:] 
                if msg['role'] == 'assistant'
            ]
            
            if recent_assistant_responses:
                # Extract key terms from recent responses
                recent_text = " ".join(recent_assistant_responses)
                nutrition_terms = ['protein', 'carbs', 'fat', 'vitamins', 'minerals', 'calories', 'fiber']
                mentioned_terms = [term for term in nutrition_terms if term in recent_text.lower()]
                
                if mentioned_terms:
                    enhanced_query = f"{query} related to {' '.join(mentioned_terms)}"
        
        # Use existing retrieval method with enhanced query
        base_results = self.vector_store.similarity_search(enhanced_query, n_results=5)
        
        # If this is a follow-up, also search for the original query terms
        if strategy.get("follow_up_question") and history:
            original_results = self.vector_store.similarity_search(query, n_results=3)
            base_results.extend(original_results)
        
        # Remove duplicates and rank by relevance
        seen_ids = set()
        unique_results = []
        for result in base_results:
            if result["id"] not in seen_ids and result["similarity"] > 0.1:
                unique_results.append(result)
                seen_ids.add(result["id"])
        
        unique_results.sort(key=lambda x: x["similarity"], reverse=True)
        return unique_results[:6]  # Limit context
    
    def _generate_conversational_response(
        self,
        query: str,
        context_docs: List[Dict],
        conversation_history: List[Dict],
        user_context: Optional[Dict],
        response_style: str
    ) -> str:
        """Generate conversational response with memory"""
        
        # Build conversation context
        conversation_context = ""
        if conversation_history and len(conversation_history) >= 2:
            # Include last 2-3 exchanges for context
            recent_history = conversation_history[-6:]  # Last 6 messages (3 exchanges)
            
            formatted_history = []
            for msg in recent_history:
                role = "You" if msg['role'] == 'user' else "Assistant"
                content = msg['content'][:150] + "..." if len(msg['content']) > 150 else msg['content']
                formatted_history.append(f"{role}: {content}")
            
            if formatted_history:
                conversation_context = f"\nRECENT CONVERSATION:\n" + "\n".join(formatted_history) + "\n"
        
        # Build nutrition context
        nutrition_context = self._build_context_string(context_docs)
        
        # Build user context
        user_context_str = ""
        if user_context:
            user_context_str = f"\nUSER PROFILE:\n{self._format_user_context(user_context)}\n"
        
        # Response style instructions
        style_instructions = {
            "brief": "Provide a concise, conversational response in 2-3 sentences. Reference our conversation when relevant.",
            "comprehensive": "Provide a thorough, conversational explanation with practical recommendations. Build on our previous discussion.",
            "detailed": "Provide an in-depth, conversational response with detailed explanations and comprehensive guidance. Reference and expand on our conversation."
        }
        
        style_instruction = style_instructions.get(response_style, style_instructions["comprehensive"])
        
        # Create conversational prompt
        user_prompt = f"""NUTRITION DATABASE CONTEXT:
{nutrition_context}
{conversation_context}
{user_context_str}
CURRENT QUESTION: {query}

RESPONSE INSTRUCTIONS: {style_instruction}

Please provide a helpful, conversational response that acknowledges our ongoing discussion and uses the nutrition database context."""
        
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
            return "I'm having trouble processing your question right now. Could you try asking again or rephrase your question?"
    
    def _build_context_string(self, context_docs: List[Dict]) -> str:
        """Build formatted context string from retrieved documents"""
        if not context_docs:
            return "No specific nutrition database context found for this query."
        
        context_parts = []
        for i, doc in enumerate(context_docs, 1):
            doc_type = doc["metadata"].get("doc_type", "unknown")
            
            if doc_type == "food_item":
                food_name = doc["metadata"].get("food_name", "Unknown Food")
                context_parts.append(f"{i}. FOOD: {food_name}\n   {doc['content']}\n")
            elif doc_type == "nutrition_knowledge":
                topic = doc["metadata"].get("topic", "Nutrition Info")
                context_parts.append(f"{i}. GUIDELINE: {topic}\n   {doc['content']}\n")
            else:
                context_parts.append(f"{i}. INFO: {doc['content']}\n")
        
        return "\n".join(context_parts)
    
    def _format_user_context(self, user_context: Dict) -> str:
        """Format user context for conversational use"""
        context_parts = []
        if "age" in user_context: context_parts.append(f"Age: {user_context['age']}")
        if "gender" in user_context: context_parts.append(f"Gender: {user_context['gender']}")
        if "goals" in user_context: context_parts.append(f"Goals: {user_context['goals']}")
        if "activity_level" in user_context: context_parts.append(f"Activity: {user_context['activity_level']}")
        if "dietary_restrictions" in user_context: context_parts.append(f"Restrictions: {user_context['dietary_restrictions']}")
        
        return " | ".join(context_parts)

# Example usage
def test_conversational_rag():
    """Test the conversational RAG engine"""
    print("🧪 Testing Conversational RAG Engine...")
    
    rag = ConversationalRAGEngine(use_local_embeddings=True)
    
    # Simulate a conversation
    conversation = [
        {"role": "user", "content": "I want to build muscle, what should I eat?"},
        {"role": "assistant", "content": "For muscle building, focus on protein sources like chicken breast, fish, and legumes..."},
        {"role": "user", "content": "Tell me more about protein timing"}
    ]
    
    response = rag.generate_conversational_response(
        current_query="Tell me more about protein timing",
        conversation_history=conversation[:-1],  # Previous messages
        response_style="comprehensive"
    )
    
    print(f"✅ Conversational response generated!")
    print(f"📊 Context used: {response['context_count']} documents")
    print(f"💬 Response preview: {response['response'][:100]}...")
    
    return response

if __name__ == "__main__":
    test_conversational_rag()