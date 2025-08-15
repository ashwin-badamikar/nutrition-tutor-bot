"""
Conversational Nutrition Coach Engine
Natural ChatGPT-style conversations with intelligent RAG integration
"""

import openai
from typing import List, Dict, Optional
import logging
import sys
import os
from pathlib import Path

# Fix imports when running from models directory
current_dir = Path(__file__).parent
parent_dir = current_dir.parent
sys.path.append(str(parent_dir))

from vector_store import VectorStoreManager  # Local import
from config.settings import settings

logger = logging.getLogger(__name__)

# Rest of the code stays the same...

class ConversationalNutritionCoach:
    def __init__(self, use_local_embeddings: bool = True):
        """Initialize conversational nutrition coach"""
        self.vector_store = VectorStoreManager(use_local_embeddings)
        openai.api_key = settings.openai_api_key
        
        # Natural conversation system prompt
        self.system_prompt = """You are a friendly, professional nutrition coach having a natural conversation. Your personality:

🎯 CONVERSATION STYLE:
- Warm, approachable, and encouraging
- Ask follow-up questions to understand needs better
- Use conversational language (not formal/clinical)
- Remember and reference what the user mentioned earlier
- Guide conversations toward helpful nutrition advice naturally

🧠 EXPERTISE AREAS:
- General nutrition and healthy eating
- Weight management (loss/gain)
- Sports nutrition and performance
- Meal planning and preparation
- Dietary restrictions and preferences
- Food relationships and habits

💬 CONVERSATION APPROACH:
- Start with understanding their situation and goals
- Ask clarifying questions when helpful
- Provide specific, actionable advice
- Use nutrition database knowledge when relevant
- Keep responses conversational and personalized
- End with questions or next steps to continue dialogue

🎨 RESPONSE TONE:
- Supportive and non-judgmental
- Educational but not overwhelming
- Practical and realistic
- Encouraging and motivating

Remember: You're having a natural conversation, not giving formal consultations. Be human, be helpful, be encouraging!"""
    
    def chat(
        self,
        user_message: str,
        conversation_history: List[Dict] = None,
        user_profile: Optional[Dict] = None,
        response_style: str = "conversational"
    ) -> Dict:
        """
        Generate natural conversational response
        
        Args:
            user_message: Current user message
            conversation_history: Previous chat messages
            user_profile: User information for personalization
            response_style: Conversation style preference
        
        Returns:
            Response with conversation metadata
        """
        try:
            # Step 1: Decide if we need nutrition database context
            needs_nutrition_context = self._should_use_nutrition_context(user_message, conversation_history)
            
            # Step 2: Get relevant nutrition context if needed
            nutrition_context = ""
            sources_used = []
            
            if needs_nutrition_context:
                context_docs = self._get_smart_nutrition_context(user_message, conversation_history)
                nutrition_context = self._format_nutrition_context(context_docs)
                sources_used = [doc["metadata"] for doc in context_docs]
            
            # Step 3: Build conversational prompt
            conversation_prompt = self._build_conversation_prompt(
                user_message,
                conversation_history,
                user_profile,
                nutrition_context,
                response_style
            )
            
            # Step 4: Generate natural response
            response_text = self._generate_natural_response(conversation_prompt)
            
            return {
                "response": response_text,
                "sources": sources_used,
                "context_used": bool(nutrition_context),
                "conversation_type": self._classify_conversation_type(user_message),
                "needs_followup": self._suggest_followup(response_text, user_message)
            }
            
        except Exception as e:
            logger.error(f"Error in conversational coach: {e}")
            return {
                "response": "I'm having a bit of trouble right now, but I'm here to help with your nutrition questions! Could you tell me what you're most interested in learning about?",
                "sources": [],
                "error": str(e)
            }
    
    def _should_use_nutrition_context(self, message: str, history: List[Dict] = None) -> bool:
        """Decide if we need to search nutrition database"""
        message_lower = message.lower()
        
        # Always use context for specific nutrition questions
        nutrition_indicators = [
            "protein", "calories", "vitamins", "minerals", "carbs", "fat", "fiber",
            "nutrition", "diet", "meal", "food", "eat", "weight loss", "muscle",
            "breakfast", "lunch", "dinner", "snack", "recipe", "ingredient"
        ]
        
        # Use context if message contains nutrition terms
        if any(term in message_lower for term in nutrition_indicators):
            return True
        
        # Use context if conversation has been about nutrition
        if history and len(history) >= 2:
            recent_nutrition_discussion = False
            for msg in history[-4:]:  # Check last 4 messages
                if msg['role'] == 'assistant':
                    content = msg['content'].lower()
                    if any(term in content for term in nutrition_indicators):
                        recent_nutrition_discussion = True
                        break
            
            if recent_nutrition_discussion:
                return True
        
        # Don't use context for greetings or general chat
        general_chat = ["hi", "hello", "hey", "thanks", "thank you", "okay", "ok", "yes", "no"]
        if message_lower.strip() in general_chat:
            return False
        
        # Use context by default for anything else
        return True
    
    def _get_smart_nutrition_context(self, message: str, history: List[Dict] = None) -> List[Dict]:
        """Get relevant nutrition context intelligently"""
        
        # Build search query from current message
        search_query = message
        
        # Enhance with conversation context if available
        if history:
            # Extract nutrition topics from recent conversation
            nutrition_topics = []
            for msg in history[-6:]:  # Last 6 messages
                content = msg['content'].lower()
                if 'protein' in content: nutrition_topics.append('protein')
                if 'weight' in content: nutrition_topics.append('weight management')
                if 'muscle' in content: nutrition_topics.append('muscle building')
                if 'meal' in content: nutrition_topics.append('meal planning')
            
            if nutrition_topics:
                search_query += f" {' '.join(set(nutrition_topics))}"
        
        # Search for relevant context (fewer results for more focused responses)
        try:
            results = self.vector_store.similarity_search(search_query, n_results=3)
            return [r for r in results if r['similarity'] > 0.2]  # Only use relevant results
        except Exception as e:
            logger.error(f"Error retrieving nutrition context: {e}")
            return []
    
    def _format_nutrition_context(self, context_docs: List[Dict]) -> str:
        """Format nutrition context for natural conversation"""
        if not context_docs:
            return ""
        
        context_parts = []
        for doc in context_docs:
            doc_type = doc["metadata"].get("doc_type", "")
            
            if doc_type == "food_item":
                food_name = doc["metadata"].get("food_name", "")
                content = doc['content']
                context_parts.append(f"FOOD INFO - {food_name}: {content}")
            
            elif doc_type == "nutrition_knowledge":
                topic = doc["metadata"].get("topic", "")
                content = doc['content']
                context_parts.append(f"NUTRITION SCIENCE - {topic}: {content}")
            
            else:
                context_parts.append(f"NUTRITION INFO: {doc['content']}")
        
        return "\n\n".join(context_parts)
    
    def _build_conversation_prompt(
        self,
        current_message: str,
        history: List[Dict],
        profile: Optional[Dict],
        nutrition_context: str,
        style: str
    ) -> str:
        """Build natural conversation prompt"""
        
        # Build conversation history
        conversation_text = ""
        if history:
            recent_history = history[-10:]  # Last 10 messages for context
            for msg in recent_history:
                role = "User" if msg['role'] == 'user' else "Nutrition Coach"
                conversation_text += f"{role}: {msg['content']}\n"
        
        # Build user profile context
        profile_text = ""
        if profile:
            profile_text = f"\nUSER PROFILE: {profile.get('age')}y/o {profile.get('gender')}, {profile.get('activity_level')}, Goal: {profile.get('goals')}"
            if profile.get('dietary_restrictions'):
                profile_text += f", Restrictions: {profile['dietary_restrictions']}"
            if profile.get('preferences'):
                profile_text += f", Preferences: {profile['preferences']}"
        
        # Build nutrition context
        nutrition_text = ""
        if nutrition_context:
            nutrition_text = f"\n\nNUTRITION DATABASE KNOWLEDGE (use when relevant):\n{nutrition_context}"
        
        # Style instructions
        style_instructions = {
            "conversational": "Respond naturally and conversationally. Ask follow-up questions to keep the dialogue flowing.",
            "brief": "Keep your response concise but friendly and conversational.",
            "comprehensive": "Provide detailed information while maintaining a natural, conversational tone."
        }
        
        style_instruction = style_instructions.get(style, style_instructions["conversational"])
        
        # Complete prompt
        prompt = f"""CONVERSATION HISTORY:
{conversation_text}

CURRENT USER MESSAGE: {current_message}
{profile_text}
{nutrition_text}

INSTRUCTIONS: {style_instruction}

Respond as a friendly nutrition coach. Be natural and conversational. Use the nutrition database knowledge when it's relevant to help answer questions, but don't force it into every response. Ask questions to understand their needs better."""
        
        return prompt
    
    def _generate_natural_response(self, prompt: str) -> str:
        """Generate natural conversational response"""
        try:
            response = openai.chat.completions.create(
                model=settings.openai_model,
                messages=[
                    {"role": "system", "content": self.system_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=settings.max_tokens,
                temperature=0.8,  # Slightly higher for more natural conversation
                presence_penalty=0.1,  # Encourage varied responses
                frequency_penalty=0.1  # Reduce repetition
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"Error generating response: {e}")
            return "I'm having a bit of trouble connecting right now, but I'm here to help! What would you like to know about nutrition?"
    
    def _classify_conversation_type(self, message: str) -> str:
        """Classify the type of conversation for analytics"""
        message_lower = message.lower()
        
        if any(word in message_lower for word in ["hi", "hello", "hey"]):
            return "greeting"
        elif any(word in message_lower for word in ["thanks", "thank you"]):
            return "appreciation"
        elif any(word in message_lower for word in ["protein", "muscle", "building"]):
            return "muscle_building"
        elif any(word in message_lower for word in ["weight", "lose", "loss"]):
            return "weight_loss"
        elif any(word in message_lower for word in ["meal", "plan", "breakfast", "dinner"]):
            return "meal_planning"
        elif "?" in message:
            return "question"
        else:
            return "general_discussion"
    
    def _suggest_followup(self, response: str, user_message: str) -> List[str]:
        """Suggest natural follow-up questions"""
        response_lower = response.lower()
        message_lower = user_message.lower()
        
        suggestions = []
        
        # Context-aware suggestions based on response content
        if 'protein' in response_lower:
            suggestions.extend([
                "How much protein do I need daily?",
                "When should I eat protein?",
                "What are the best protein sources for me?"
            ])
        
        if 'weight loss' in response_lower:
            suggestions.extend([
                "How fast should I lose weight?",
                "What foods should I avoid?",
                "Can you help me plan my meals?"
            ])
        
        if 'meal' in response_lower or 'breakfast' in response_lower:
            suggestions.extend([
                "Can you suggest specific recipes?",
                "What about meal prep ideas?",
                "How do I make this work with my schedule?"
            ])
        
        # General helpful follow-ups
        if not suggestions:
            suggestions = [
                "Can you give me specific examples?",
                "How do I get started with this?",
                "What should I focus on first?",
                "Any tips for staying consistent?"
            ]
        
        return suggestions[:3]  # Return top 3 suggestions

# Test function
def test_conversational_coach():
    """Test the conversational nutrition coach"""
    print("🧪 Testing Conversational Nutrition Coach...")
    
    coach = ConversationalNutritionCoach(use_local_embeddings=True)
    
    # Test conversation flow
    test_conversation = [
        {"role": "user", "content": "hi"},
        {"role": "assistant", "content": "Hi! I'm your nutrition coach. What brings you here today?"},
        {"role": "user", "content": "I want to lose weight"},
    ]
    
    response = coach.chat(
        user_message="I want to lose weight",
        conversation_history=test_conversation[:-1],
        response_style="conversational"
    )
    
    print(f"✅ Natural response generated!")
    print(f"💬 Response: {response['response'][:100]}...")
    print(f"📊 Context used: {response['context_used']}")
    print(f"📝 Conversation type: {response['conversation_type']}")
    
    return response

if __name__ == "__main__":
    test_conversational_coach()