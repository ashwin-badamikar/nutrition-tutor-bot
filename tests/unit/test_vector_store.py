"""
Unit tests for Vector Store (ChromaDB) functionality
Tests embedding, storage, and similarity search capabilities
"""

import pytest
import sys
import os
import tempfile
import shutil
from pathlib import Path
from unittest.mock import patch, Mock

# Add src to path for imports
sys.path.append(str(Path(__file__).parent.parent.parent / 'src'))

from models.vector_store import VectorStoreManager

class TestVectorStoreManager:
    """Test suite for Vector Store functionality"""
    
    @pytest.fixture
    def temp_db_path(self):
        """Create temporary database path for testing"""
        temp_dir = tempfile.mkdtemp()
        yield temp_dir
        # Cleanup after test
        shutil.rmtree(temp_dir, ignore_errors=True)
    
    @pytest.fixture
    def vector_store(self, temp_db_path):
        """Create vector store instance for testing"""
        with patch('models.vector_store.Path') as mock_path:
            # Mock the database path to use temp directory
            mock_path.return_value = temp_db_path
            vs = VectorStoreManager(use_local_embeddings=True)
            return vs
    
    def test_initialization(self, vector_store):
        """Test vector store initialization"""
        assert vector_store is not None
        assert vector_store.use_local_embeddings == True
        assert vector_store.embedding_dimension == 384
        assert hasattr(vector_store, 'embedding_model')
        assert hasattr(vector_store, 'client')
    
    def test_get_embeddings_local(self, vector_store):
        """Test local embedding generation"""
        test_texts = ["chicken breast nutrition", "protein sources"]
        embeddings = vector_store.get_embeddings(test_texts)
        
        assert embeddings.shape[0] == 2  # Two texts
        assert embeddings.shape[1] == 384  # Embedding dimension
        assert embeddings.dtype.name.startswith('float')  # Float values
    
    def test_embedding_similarity(self, vector_store):
        """Test that similar texts have similar embeddings"""
        similar_texts = ["chicken breast", "chicken meat"]
        different_texts = ["chicken breast", "apple fruit"]
        
        similar_embeddings = vector_store.get_embeddings(similar_texts)
        different_embeddings = vector_store.get_embeddings(different_texts)
        
        # Calculate cosine similarity
        def cosine_similarity(a, b):
            return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
        
        import numpy as np
        similar_score = cosine_similarity(similar_embeddings[0], similar_embeddings[1])
        different_score = cosine_similarity(different_embeddings[0], different_embeddings[1])
        
        # Similar texts should have higher similarity than different texts
        assert similar_score > different_score
    
    @patch('json.load')
    @patch('pathlib.Path.exists')
    def test_load_and_embed_documents(self, mock_exists, mock_json_load, vector_store):
        """Test document loading and embedding process"""
        # Mock document data
        mock_exists.return_value = True
        mock_documents = [
            {
                "id": "food_001",
                "type": "food_item", 
                "content": "Chicken breast contains high protein and low fat",
                "metadata": {
                    "food_name": "Chicken Breast",
                    "calories": 165,
                    "protein": 31
                }
            },
            {
                "id": "knowledge_001",
                "type": "nutrition_knowledge",
                "content": "Protein is essential for muscle building and repair",
                "metadata": {
                    "topic": "Protein Benefits",
                    "category": "Nutrition Science"
                }
            }
        ]
        mock_json_load.return_value = mock_documents
        
        # Test loading
        with patch.object(vector_store.collection, 'add') as mock_add:
            success = vector_store.load_and_embed_documents()
            
            assert success == True
            mock_add.assert_called_once()
            
            # Verify the call arguments
            call_args = mock_add.call_args
            assert len(call_args[1]['embeddings']) == 2
            assert len(call_args[1]['documents']) == 2
            assert len(call_args[1]['ids']) == 2
    
    def test_similarity_search_basic(self, vector_store):
        """Test basic similarity search functionality"""
        # Mock the collection query method
        with patch.object(vector_store.collection, 'query') as mock_query:
            mock_query.return_value = {
                'documents': [['Chicken breast is high in protein']],
                'metadatas': [[{'food_name': 'Chicken Breast', 'calories': '165'}]],
                'distances': [[0.2]],
                'ids': [['food_001']]
            }
            
            results = vector_store.similarity_search("high protein food", n_results=1)
            
            assert len(results) == 1
            assert results[0]['content'] == 'Chicken breast is high in protein'
            assert results[0]['metadata']['food_name'] == 'Chicken Breast'
            assert results[0]['similarity'] > 0.7  # 1 - 0.2 = 0.8
    
    def test_similarity_search_with_filter(self, vector_store):
        """Test similarity search with metadata filtering"""
        with patch.object(vector_store.collection, 'query') as mock_query:
            mock_query.return_value = {
                'documents': [['High protein chicken breast nutrition']],
                'metadatas': [[{'doc_type': 'food_item', 'food_name': 'Chicken'}]],
                'distances': [[0.1]],
                'ids': [['food_001']]
            }
            
            # Test with filter
            results = vector_store.similarity_search(
                "protein", 
                n_results=5, 
                filter_dict={"doc_type": "food_item"}
            )
            
            assert len(results) == 1
            assert results[0]['metadata']['doc_type'] == 'food_item'
            
            # Verify filter was passed to query
            mock_query.assert_called_once()
            call_args = mock_query.call_args
            assert call_args[1]['where'] == {"doc_type": "food_item"}
    
    def test_hybrid_search_food_focus(self, vector_store):
        """Test hybrid search with food focus"""
        with patch.object(vector_store, 'similarity_search') as mock_search:
            # Mock different search results for different filters
            mock_search.side_effect = [
                [{'id': 'food_1', 'similarity': 0.9, 'content': 'Food item 1'}],
                [{'id': 'knowledge_1', 'similarity': 0.7, 'content': 'Knowledge item 1'}]
            ]
            
            results = vector_store.hybrid_search(
                "protein foods", 
                n_results=4,
                food_focus=True
            )
            
            assert len(results) == 2
            assert results[0]['similarity'] >= results[1]['similarity']  # Sorted by similarity
    
    def test_get_collection_stats(self, vector_store):
        """Test collection statistics retrieval"""
        with patch.object(vector_store.collection, 'count') as mock_count:
            with patch.object(vector_store.collection, 'query') as mock_query:
                mock_count.return_value = 66
                mock_query.return_value = {
                    'metadatas': [[
                        {'doc_type': 'food_item'},
                        {'doc_type': 'food_item'},
                        {'doc_type': 'nutrition_knowledge'}
                    ]]
                }
                
                stats = vector_store.get_collection_stats()
                
                assert stats['total_documents'] == 66
                assert stats['embedding_model'] == 'local (all-MiniLM-L6-v2)'
                assert stats['embedding_dimension'] == 384
                assert 'document_types' in stats


class TestVectorStorePerformance:
    """Performance tests for vector store operations"""
    
    @pytest.fixture
    def vector_store(self):
        return VectorStoreManager(use_local_embeddings=True)
    
    @pytest.mark.benchmark
    def test_embedding_generation_performance(self, vector_store, benchmark):
        """Benchmark embedding generation speed"""
        test_texts = ["chicken breast nutrition facts"] * 10
        
        def embedding_operation():
            return vector_store.get_embeddings(test_texts)
        
        result = benchmark(embedding_operation)
        assert result.shape[0] == 10
        assert result.shape[1] == 384
    
    @pytest.mark.benchmark
    def test_similarity_search_performance(self, vector_store, benchmark):
        """Benchmark similarity search speed"""
        with patch.object(vector_store.collection, 'query') as mock_query:
            mock_query.return_value = {
                'documents': [['Sample food document']],
                'metadatas': [[{'doc_type': 'food_item'}]],
                'distances': [[0.3]],
                'ids': [['food_001']]
            }
            
            def search_operation():
                return vector_store.similarity_search("protein", n_results=5)
            
            result = benchmark(search_operation)
            assert len(result) == 1


if __name__ == "__main__":
    # Run specific tests
    pytest.main([__file__, "-v", "--benchmark-only"])