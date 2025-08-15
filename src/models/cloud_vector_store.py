"""
Fast Deployment Vector Store
Lightweight vector search without heavy model downloads
"""

import json
import numpy as np
from typing import List, Dict, Optional
from pathlib import Path
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class FastVectorStore:
    def __init__(self):
        """Initialize fast vector store with TF-IDF (no model download needed)"""
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.documents = []
        self.document_vectors = None
        self.is_fitted = False
        
        # Load and initialize immediately
        self.load_and_embed_documents()
    
    def load_and_embed_documents(self) -> bool:
        """Load nutrition documents and create TF-IDF vectors"""
        try:
            # Create comprehensive nutrition documents
            self.documents = [
                {
                    "id": "food_001",
                    "type": "food_item",
                    "content": "Chicken breast skinless contains 165 calories and 31g protein per 100g serving. Excellent lean protein source for muscle building and weight management.",
                    "metadata": {"food_name": "Chicken Breast", "calories": "165", "protein": "31", "doc_type": "food_item", "category": "Poultry"}
                },
                {
                    "id": "food_002", 
                    "type": "food_item",
                    "content": "Salmon Atlantic provides 208 calories and 25g protein per 100g. Rich in omega-3 fatty acids for heart health and brain function.",
                    "metadata": {"food_name": "Salmon", "calories": "208", "protein": "25", "doc_type": "food_item", "category": "Seafood"}
                },
                {
                    "id": "food_003",
                    "type": "food_item", 
                    "content": "Broccoli raw contains 34 calories and 2.8g protein per 100g. High in vitamin C, fiber, and antioxidants for immune support.",
                    "metadata": {"food_name": "Broccoli", "calories": "34", "protein": "2.8", "doc_type": "food_item", "category": "Vegetables"}
                },
                {
                    "id": "knowledge_001",
                    "type": "nutrition_knowledge",
                    "content": "Protein requirements vary by activity level. Sedentary adults need 0.8g per kg body weight daily. Athletes require 1.2-2.2g per kg for muscle building and recovery.",
                    "metadata": {"topic": "Protein Requirements", "category": "Macronutrients", "doc_type": "nutrition_knowledge"}
                },
                {
                    "id": "knowledge_002",
                    "type": "nutrition_knowledge",
                    "content": "Weight loss requires caloric deficit of 500-750 calories daily for safe 1-2 pound weekly loss. Combine moderate calorie restriction with regular exercise.",
                    "metadata": {"topic": "Weight Loss", "category": "Weight Management", "doc_type": "nutrition_knowledge"}
                },
                {
                    "id": "knowledge_003",
                    "type": "nutrition_knowledge",
                    "content": "Post-workout nutrition window extends 24-48 hours, not just 30 minutes. Consume protein within 2 hours post-exercise for optimal muscle protein synthesis.",
                    "metadata": {"topic": "Sports Nutrition", "category": "Exercise Nutrition", "doc_type": "nutrition_knowledge"}
                }
            ]
            
            # Extract text content for vectorization
            texts = [doc["content"] for doc in self.documents]
            
            # Create TF-IDF vectors (fast, no model download)
            self.document_vectors = self.vectorizer.fit_transform(texts)
            self.is_fitted = True
            
            logger.info(f"Successfully loaded {len(self.documents)} documents with TF-IDF vectors")
            return True
            
        except Exception as e:
            logger.error(f"Error loading documents: {e}")
            return False
    
    def similarity_search(self, query: str, n_results: int = 5, filter_dict: Optional[Dict] = None) -> List[Dict]:
        """Fast similarity search using TF-IDF"""
        try:
            if not self.is_fitted:
                return []
            
            # Transform query to vector
            query_vector = self.vectorizer.transform([query])
            
            # Calculate similarities
            similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
            
            # Get top results
            top_indices = similarities.argsort()[-n_results:][::-1]
            
            results = []
            for idx in top_indices:
                if similarities[idx] > 0.01:  # Minimum similarity threshold
                    doc = self.documents[idx]
                    
                    # Apply filter if specified
                    if filter_dict:
                        match = True
                        for key, value in filter_dict.items():
                            if doc["metadata"].get(key) != value:
                                match = False
                                break
                        if not match:
                            continue
                    
                    result = {
                        "content": doc["content"],
                        "metadata": doc["metadata"],
                        "similarity": float(similarities[idx]),
                        "id": doc["id"]
                    }
                    results.append(result)
            
            return results[:n_results]
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        return {
            "total_documents": len(self.documents),
            "embedding_model": "TF-IDF (fast deployment)",
            "embedding_dimension": self.document_vectors.shape[1] if self.document_vectors is not None else 0,
            "storage_mode": "in-memory"
        }

# For compatibility with your existing code
class CloudVectorStoreManager(FastVectorStore):
    def __init__(self, use_local_embeddings=True):
        super().__init__()