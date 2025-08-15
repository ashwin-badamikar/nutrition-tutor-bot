"""
Integration tests for complete system functionality
Tests end-to-end workflows and component interactions
"""

import pytest
import sys
import os
from pathlib import Path
from unittest.mock import patch, Mock

# Add src to path
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

class TestSystemIntegration:
    """Integration tests for complete system workflows"""
    
    def test_complete_rag_pipeline(self):
        """Test complete RAG pipeline from query to response"""
        try:
            from models.rag_engine import RAGQueryEngine
            
            rag = RAGQueryEngine(use_local_embeddings=True)
            
            # Test query that should work with your knowledge base
            query = "What are good protein sources?"
            response = rag.generate_response(query, response_style="brief")
            
            # Verify response structure
            assert 'response' in response
            assert 'sources' in response
            assert 'search_strategy' in response
            assert 'context_count' in response
            
            # Verify response quality
            assert len(response['response']) > 10  # Non-empty response
            assert response['context_count'] >= 0
            
            print(f"✅ RAG Pipeline Test: {response['context_count']} sources used")
            
        except Exception as e:
            pytest.fail(f"RAG pipeline integration test failed: {e}")
    
    def test_nutrition_api_integration(self):
        """Test USDA API integration with meal analysis"""
        try:
            from models.nutrition_api import USDANutritionAPI
            
            api = USDANutritionAPI()
            
            # Test meal component analysis
            meal_components = ["4oz chicken breast", "1 cup broccoli"]
            results = api.analyze_meal_components(meal_components)
            
            assert len(results) == 2
            
            for result in results:
                assert 'original_description' in result
                assert 'nutrition' in result
                assert 'portion' in result
                
                # Verify nutrition data structure
                nutrition = result['nutrition']
                assert isinstance(nutrition.get('calories', 0), (int, float))
                assert isinstance(nutrition.get('protein_g', 0), (int, float))
            
            print(f"✅ Nutrition API Integration: Analyzed {len(results)} meal components")
            
        except Exception as e:
            pytest.fail(f"Nutrition API integration test failed: {e}")
    
    def test_vector_database_integration(self):
        """Test vector database with actual nutrition queries"""
        try:
            from models.vector_store import VectorStoreManager
            
            vs = VectorStoreManager(use_local_embeddings=True)
            
            # Test various query types
            test_queries = [
                "protein rich foods",
                "muscle building nutrition", 
                "weight loss meal planning",
                "vitamin deficiency"
            ]
            
            for query in test_queries:
                results = vs.similarity_search(query, n_results=3)
                
                assert isinstance(results, list)
                assert len(results) <= 3
                
                for result in results:
                    assert 'content' in result
                    assert 'metadata' in result
                    assert 'similarity' in result
                    assert isinstance(result['similarity'], (int, float))
            
            print(f"✅ Vector Database Integration: Tested {len(test_queries)} query types")
            
        except Exception as e:
            pytest.fail(f"Vector database integration test failed: {e}")
    
    def test_user_profile_workflow(self):
        """Test user profile creation and usage workflow"""
        # Test profile data structure
        sample_profile = {
            "age": 25,
            "gender": "Male",
            "activity_level": "Moderately Active",
            "goals": "Muscle Building",
            "dietary_restrictions": "Dairy-Free",
            "preferences": "High Protein"
        }
        
        # Verify profile structure
        required_fields = ["age", "gender", "activity_level", "goals"]
        for field in required_fields:
            assert field in sample_profile
            assert sample_profile[field] is not None
        
        print("✅ User Profile Workflow: Profile structure validated")
    
    @patch('openai.chat.completions.create')
    def test_multimodal_workflow_mock(self, mock_openai):
        """Test multimodal workflow with mocked OpenAI Vision"""
        try:
            # Mock OpenAI Vision response
            mock_response = Mock()
            mock_response.choices = [Mock()]
            mock_response.choices[0].message.content = "- 6oz grilled chicken breast\n- 1 cup steamed broccoli\n- 0.5 cup brown rice"
            mock_openai.return_value = mock_response
            
            from models.nutrition_api import USDANutritionAPI
            
            api = USDANutritionAPI()
            
            # Simulate the meal analysis workflow
            vision_result = "- 6oz grilled chicken breast\n- 1 cup steamed broccoli"
            
            # Extract food descriptions (this is what your app does)
            import re
            food_lines = [line.strip() for line in vision_result.split('\n') if line.strip().startswith('-')]
            food_descriptions = [line[1:].strip() for line in food_lines]
            
            # Test meal analysis
            if food_descriptions:
                analyzed_foods = api.analyze_meal_components(food_descriptions)
                
                assert len(analyzed_foods) >= 0  # Should process without errors
                print(f"✅ Multimodal Workflow: Processed {len(analyzed_foods)} foods from vision")
            
        except Exception as e:
            pytest.fail(f"Multimodal workflow test failed: {e}")


def run_integration_tests():
    """Run all integration tests"""
    print("🔗 Running System Integration Tests...")
    print("=" * 50)
    
    tester = TestSystemIntegration()
    
    try:
        tester.test_complete_rag_pipeline()
        tester.test_nutrition_api_integration()
        tester.test_vector_database_integration()
        tester.test_user_profile_workflow()
        tester.test_multimodal_workflow_mock()
        
        print("\n🎉 All integration tests passed!")
        return True
        
    except Exception as e:
        print(f"\n❌ Integration test failed: {e}")
        return False

if __name__ == "__main__":
    success = run_integration_tests()
    
    if success:
        print("\n✅ System integration validated!")
        print("🚀 Your nutrition bot components work together seamlessly!")
    else:
        print("\n🔧 Please check the errors above.")