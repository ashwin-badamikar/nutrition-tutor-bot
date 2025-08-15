"""
Fast Vector Store for Cloud Deployment
Uses TF-IDF instead of heavy sentence-transformers
"""

import numpy as np
from typing import List, Dict, Optional
import logging
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, use_local_embeddings=True):
        """Fast vector store using TF-IDF"""
        self.vectorizer = TfidfVectorizer(max_features=1000, stop_words='english')
        self.documents = self._create_nutrition_documents()
        self.document_vectors = None
        self.load_and_embed_documents()
    
    def _create_nutrition_documents(self):
        """Create nutrition documents"""
        return [
            {
                "id": "food_001",
                "content": "Chicken breast contains 165 calories and 31g protein per 100g. Excellent lean protein for muscle building.",
                "metadata": {"food_name": "Chicken Breast", "calories": "165", "protein": "31", "doc_type": "food_item"}
            },
            {
                "id": "knowledge_001", 
                "content": "Protein requirements: 0.8-2.2g per kg body weight daily depending on activity level and goals.",
                "metadata": {"topic": "Protein Requirements", "doc_type": "nutrition_knowledge"}
            },
            {
                "id": "knowledge_002",
                "content": "Weight loss: Create 500-750 calorie daily deficit for healthy 1-2 pound weekly weight loss.",
                "metadata": {"topic": "Weight Loss", "doc_type": "nutrition_knowledge"}
            }
        ]
    
    def load_and_embed_documents(self):
        """Create TF-IDF vectors (fast)"""
        texts = [doc["content"] for doc in self.documents]
        self.document_vectors = self.vectorizer.fit_transform(texts)
        return True
    
    def similarity_search(self, query: str, n_results: int = 5, filter_dict: Optional[Dict] = None):
        """Fast similarity search"""
        query_vector = self.vectorizer.transform([query])
        similarities = cosine_similarity(query_vector, self.document_vectors).flatten()
        top_indices = similarities.argsort()[-n_results:][::-1]
        
        results = []
        for idx in top_indices:
            if similarities[idx] > 0.01:
                doc = self.documents[idx]
                results.append({
                    "content": doc["content"],
                    "metadata": doc["metadata"], 
                    "similarity": float(similarities[idx]),
                    "id": doc["id"]
                })
        return results
    
    def get_collection_stats(self):
        """Get stats"""
        return {
            "total_documents": len(self.documents),
            "embedding_model": "TF-IDF (fast)",
            "embedding_dimension": self.document_vectors.shape[1] if self.document_vectors is not None else 0
        }