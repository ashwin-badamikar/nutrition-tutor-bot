"""
Cloud-Compatible Vector Store for Streamlit Deployment
Uses ChromaDB in memory mode to avoid SQLite version conflicts
"""

import json
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import logging
from sentence_transformers import SentenceTransformer
import chromadb
import openai
import os

logger = logging.getLogger(__name__)

class CloudVectorStoreManager:
    def __init__(self, use_local_embeddings: bool = True):
        """
        Initialize cloud-compatible vector store manager
        Uses in-memory ChromaDB to avoid SQLite issues
        """
        self.use_local_embeddings = use_local_embeddings
        self.data_path = Path("data/processed")
        
        # Initialize embedding model
        if use_local_embeddings:
            logger.info("Loading local embedding model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_dimension = 384
        else:
            logger.info("Using OpenAI embeddings...")
            openai.api_key = os.getenv('OPENAI_API_KEY')
            self.embedding_model = None
            self.embedding_dimension = 1536
        
        # Initialize ChromaDB in MEMORY MODE (cloud-compatible)
        try:
            self.client = chromadb.Client()  # In-memory client
            logger.info("Initialized ChromaDB in memory mode (cloud-compatible)")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB: {e}")
            # Fallback to ephemeral client
            self.client = chromadb.EphemeralClient()
            logger.info("Using ephemeral ChromaDB client")
        
        # Create collection
        self.collection_name = "nutrition_knowledge"
        try:
            self.collection = self.client.get_collection(self.collection_name)
            logger.info(f"Loaded existing collection: {self.collection_name}")
        except Exception:
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Nutrition knowledge base for RAG"}
            )
            logger.info(f"Created new collection: {self.collection_name}")
    
    def get_embeddings(self, texts: List[str]) -> np.ndarray:
        """Generate embeddings for list of texts"""
        if self.use_local_embeddings:
            return self.embedding_model.encode(texts, convert_to_tensor=False)
        else:
            # Use OpenAI embeddings
            embeddings = []
            for text in texts:
                try:
                    response = openai.embeddings.create(
                        input=text,
                        model="text-embedding-ada-002"
                    )
                    embeddings.append(response.data[0].embedding)
                except Exception as e:
                    logger.error(f"Error getting OpenAI embedding: {e}")
                    embeddings.append([0.0] * self.embedding_dimension)
            return np.array(embeddings)
    
    def load_and_embed_documents(self) -> bool:
        """Load documents and create embeddings - CLOUD COMPATIBLE"""
        try:
            # Try to load from file, fallback to creating sample data
            documents_path = self.data_path / "comprehensive_documents.json"
            
            if documents_path.exists():
                with open(documents_path, "r") as f:
                    documents = json.load(f)
            else:
                # Create sample documents for cloud deployment
                documents = self._create_sample_documents()
            
            logger.info(f"Loading {len(documents)} documents...")
            
            # Prepare data for embedding
            texts = []
            ids = []
            metadatas = []
            
            for doc in documents:
                texts.append(doc["content"])
                ids.append(doc["id"])
                
                # Clean metadata for ChromaDB
                clean_metadata = {}
                for key, value in doc["metadata"].items():
                    if isinstance(value, (str, int, float, bool)):
                        clean_metadata[key] = str(value)
                    elif isinstance(value, list):
                        clean_metadata[key] = ", ".join(map(str, value))
                    else:
                        clean_metadata[key] = str(value)
                
                clean_metadata["doc_type"] = doc["type"]
                metadatas.append(clean_metadata)
            
            # Generate embeddings in batches
            batch_size = 50
            all_embeddings = []
            
            for i in range(0, len(texts), batch_size):
                batch_texts = texts[i:i + batch_size]
                batch_embeddings = self.get_embeddings(batch_texts)
                all_embeddings.extend(batch_embeddings.tolist())
                logger.info(f"Embedded batch {i//batch_size + 1}/{(len(texts)-1)//batch_size + 1}")
            
            # Add to ChromaDB (in-memory)
            self.collection.add(
                embeddings=all_embeddings,
                documents=texts,
                metadatas=metadatas,
                ids=ids
            )
            
            logger.info(f"Successfully embedded and stored {len(documents)} documents")
            return True
            
        except Exception as e:
            logger.error(f"Error loading and embedding documents: {e}")
            return False
    
    def similarity_search(
        self, 
        query: str, 
        n_results: int = 5,
        filter_dict: Optional[Dict] = None
    ) -> List[Dict]:
        """Search for similar documents"""
        try:
            # Generate query embedding
            query_embedding = self.get_embeddings([query])[0].tolist()
            
            # Search in ChromaDB
            results = self.collection.query(
                query_embeddings=[query_embedding],
                n_results=n_results,
                where=filter_dict
            )
            
            # Format results
            formatted_results = []
            for i in range(len(results["documents"][0])):
                result = {
                    "content": results["documents"][0][i],
                    "metadata": results["metadatas"][0][i],
                    "similarity": 1 - results["distances"][0][i] if "distances" in results else 0.0,
                    "id": results["ids"][0][i]
                }
                formatted_results.append(result)
            
            logger.info(f"Found {len(formatted_results)} relevant documents for query: '{query}'")
            return formatted_results
            
        except Exception as e:
            logger.error(f"Error in similarity search: {e}")
            return []
    
    def get_collection_stats(self) -> Dict:
        """Get statistics about the collection"""
        try:
            count = self.collection.count()
            
            return {
                "total_documents": count,
                "embedding_model": "local (all-MiniLM-L6-v2)" if self.use_local_embeddings else "OpenAI",
                "embedding_dimension": self.embedding_dimension,
                "storage_mode": "in-memory (cloud-compatible)"
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    def _create_sample_documents(self) -> List[Dict]:
        """Create sample documents if files not available in cloud"""
        return [
            {
                "id": "food_001",
                "type": "food_item",
                "content": "Chicken breast, skinless, contains 165 calories and 31g protein per 100g. Excellent source of lean protein for muscle building.",
                "metadata": {
                    "food_name": "Chicken Breast",
                    "calories": "165",
                    "protein": "31",
                    "category": "Poultry",
                    "doc_type": "food_item"
                }
            },
            {
                "id": "knowledge_001", 
                "type": "nutrition_knowledge",
                "content": "Protein Requirements: Adults need 0.8-2.2g protein per kg body weight daily depending on activity level. Athletes require higher amounts.",
                "metadata": {
                    "topic": "Protein Requirements",
                    "category": "Macronutrients",
                    "doc_type": "nutrition_knowledge"
                }
            },
            {
                "id": "knowledge_002",
                "type": "nutrition_knowledge", 
                "content": "Weight Loss: Create a caloric deficit of 500-750 calories daily for healthy 1-2 lb weekly weight loss through diet and exercise.",
                "metadata": {
                    "topic": "Weight Loss Guidelines",
                    "category": "Weight Management",
                    "doc_type": "nutrition_knowledge"
                }
            }
        ]

# Test function for cloud deployment
def test_cloud_vector_store():
    """Test the cloud-compatible vector store"""
    try:
        vs = CloudVectorStoreManager(use_local_embeddings=True)
        success = vs.load_and_embed_documents()
        
        if success:
            stats = vs.get_collection_stats()
            print(f"✅ Cloud vector store working! {stats['total_documents']} documents")
            
            # Test search
            results = vs.similarity_search("protein foods", n_results=3)
            print(f"✅ Search working! Found {len(results)} results")
            return True
        else:
            print("❌ Failed to load documents")
            return False
            
    except Exception as e:
        print(f"❌ Cloud vector store error: {e}")
        return False

if __name__ == "__main__":
    test_cloud_vector_store()