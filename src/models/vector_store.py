import json
import numpy as np
import pandas as pd
from typing import List, Dict, Optional, Tuple
from pathlib import Path
import logging
from sentence_transformers import SentenceTransformer
import chromadb
from chromadb.config import Settings
import openai
import sys
import os

# Add parent directory to path to import config
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.settings import settings

logger = logging.getLogger(__name__)

class VectorStoreManager:
    def __init__(self, use_local_embeddings: bool = True):
        """
        Initialize vector store manager
        
        Args:
            use_local_embeddings: If True, use sentence-transformers locally. 
                                If False, use OpenAI embeddings (requires API key)
        """
        self.use_local_embeddings = use_local_embeddings
        self.data_path = Path("../data/processed")
        
        # Initialize embedding model
        if use_local_embeddings:
            logger.info("Loading local embedding model...")
            self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
            self.embedding_dimension = 384
        else:
            logger.info("Using OpenAI embeddings...")
            openai.api_key = settings.openai_api_key
            self.embedding_model = None
            self.embedding_dimension = 1536
        
        # Initialize ChromaDB
        self.client = chromadb.PersistentClient(
            path="../data/chroma_db",
            settings=Settings(anonymized_telemetry=False)
        )
        
        # Create or get collection
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
                        model=settings.embedding_model
                    )
                    embeddings.append(response.data[0].embedding)
                except Exception as e:
                    logger.error(f"Error getting OpenAI embedding: {e}")
                    # Fallback to zero vector
                    embeddings.append([0.0] * self.embedding_dimension)
            return np.array(embeddings)
    
    def load_and_embed_documents(self) -> bool:
        """Load documents and create embeddings"""
        try:
            # Load processed documents
            with open(self.data_path / "comprehensive_documents.json", "r") as f:
                documents = json.load(f)
            
            logger.info(f"Loading {len(documents)} documents...")
            
            # Prepare data for embedding
            texts = []
            ids = []
            metadatas = []
            
            for doc in documents:
                texts.append(doc["content"])
                ids.append(doc["id"])
                
                # Clean metadata for ChromaDB (only string values)
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
            
            # Clear existing collection
            try:
                self.client.delete_collection(self.collection_name)
            except:
                pass
            
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Nutrition knowledge base for RAG"}
            )
            
            # Add to ChromaDB
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
        """
        Search for similar documents
        
        Args:
            query: Search query
            n_results: Number of results to return
            filter_dict: Optional filters (e.g., {"doc_type": "food_item"})
        
        Returns:
            List of relevant documents with metadata
        """
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
            
            # Get sample of metadata to understand document types
            sample_results = self.collection.query(
                query_embeddings=[self.get_embeddings(["nutrition"])[0].tolist()],
                n_results=min(20, count)
            )
            
            doc_types = {}
            for metadata in sample_results["metadatas"][0]:
                doc_type = metadata.get("doc_type", "unknown")
                doc_types[doc_type] = doc_types.get(doc_type, 0) + 1
            
            return {
                "total_documents": count,
                "document_types": doc_types,
                "embedding_model": "local (all-MiniLM-L6-v2)" if self.use_local_embeddings else "OpenAI",
                "embedding_dimension": self.embedding_dimension
            }
        except Exception as e:
            logger.error(f"Error getting collection stats: {e}")
            return {"error": str(e)}
    
    def hybrid_search(
        self, 
        query: str, 
        n_results: int = 10,
        food_focus: bool = False,
        knowledge_focus: bool = False
    ) -> List[Dict]:
        """
        Advanced search that combines different document types intelligently
        
        Args:
            query: Search query
            n_results: Total number of results
            food_focus: Prioritize food-related documents
            knowledge_focus: Prioritize knowledge/guideline documents
        """
        all_results = []
        
        if food_focus:
            # Get food-specific results
            food_results = self.similarity_search(
                query, 
                n_results=max(2, n_results//2),
                filter_dict={"doc_type": "food_item"}
            )
            all_results.extend(food_results)
            
            # Get remaining from other types
            remaining = n_results - len(food_results)
            if remaining > 0:
                other_results = self.similarity_search(
                    query,
                    n_results=remaining,
                    filter_dict={"doc_type": {"$ne": "food_item"}}
                )
                all_results.extend(other_results)
        
        elif knowledge_focus:
            # Get knowledge-specific results
            knowledge_results = self.similarity_search(
                query,
                n_results=max(2, n_results//2),
                filter_dict={"doc_type": "nutrition_knowledge"}
            )
            all_results.extend(knowledge_results)
            
            # Get remaining from other types
            remaining = n_results - len(knowledge_results)
            if remaining > 0:
                other_results = self.similarity_search(
                    query,
                    n_results=remaining
                )
                all_results.extend(other_results)
        
        else:
            # Balanced search across all document types
            all_results = self.similarity_search(query, n_results=n_results)
        
        # Remove duplicates and sort by relevance
        seen_ids = set()
        unique_results = []
        for result in all_results:
            if result["id"] not in seen_ids:
                unique_results.append(result)
                seen_ids.add(result["id"])
        
        # Sort by similarity score
        unique_results.sort(key=lambda x: x["similarity"], reverse=True)
        
        return unique_results[:n_results]

def test_vector_store():
    """Test the vector store functionality"""
    print("🧪 Testing Vector Store...")
    
    # Initialize vector store
    vs = VectorStoreManager(use_local_embeddings=True)
    
    # Load and embed documents
    success = vs.load_and_embed_documents()
    if not success:
        print("❌ Failed to load documents")
        return
    
    # Get collection stats
    stats = vs.get_collection_stats()
    print(f"📊 Collection Stats: {stats}")
    
    # Test searches
    test_queries = [
        "high protein foods for muscle building",
        "vitamin C sources for immune system", 
        "weight loss meal planning",
        "post workout nutrition"
    ]
    
    for query in test_queries:
        print(f"\n🔍 Query: '{query}'")
        results = vs.similarity_search(query, n_results=3)
        
        for i, result in enumerate(results, 1):
            print(f"   {i}. {result['metadata'].get('food_name', result['metadata'].get('topic', 'Unknown'))}")
            print(f"      Type: {result['metadata']['doc_type']}")
            print(f"      Similarity: {result['similarity']:.3f}")
    
    print("\n✅ Vector store test completed!")

if __name__ == "__main__":
    test_vector_store()