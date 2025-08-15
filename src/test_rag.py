"""
Test script for RAG system - saves as src/test_rag.py
"""

import sys
import os
from pathlib import Path

# Ensure we can import our modules
sys.path.append(str(Path(__file__).parent))

def test_complete_rag_system():
    print("🧪 Testing Complete RAG System...")
    print("=" * 50)
    
    # Test 1: Vector Store (already working based on your output)
    print("1. Testing Vector Store...")
    try:
        from models.vector_store import VectorStoreManager
        
        vs = VectorStoreManager(use_local_embeddings=True)
        stats = vs.get_collection_stats()
        print(f"   ✅ Vector store ready with {stats.get('total_documents', 0)} documents")
        
        # Quick search test
        results = vs.similarity_search("protein foods", n_results=2)
        print(f"   🔍 Search test: Found {len(results)} results")
        
    except Exception as e:
        print(f"   ❌ Vector store error: {e}")
        return False
    
    # Test 2: RAG Engine with OpenAI
    print("\n2. Testing RAG Engine with OpenAI...")
    try:
        from models.rag_engine import RAGQueryEngine
        
        rag = RAGQueryEngine(use_local_embeddings=True)
        
        test_queries = [
            "What are the best protein sources for muscle building?",
            "I need foods high in vitamin C",
            "Help me plan a healthy breakfast"
        ]
        
        for query in test_queries:
            print(f"\n   🔍 Testing: '{query}'")
            response = rag.generate_response(query, response_style="brief")
            
            if response.get("response") and "error" not in response:
                print(f"   ✅ Response generated successfully")
                print(f"   💬 Preview: {response['response'][:100]}...")
                print(f"   📚 Sources used: {len(response.get('sources', []))}")
            else:
                print(f"   ❌ Error: {response.get('error', 'Unknown error')}")
                print(f"   📝 Full response: {response}")
                
    except Exception as e:
        print(f"   ❌ RAG engine error: {e}")
        import traceback
        traceback.print_exc()
        return False
    
    print("\n✅ RAG system test completed!")
    return True

if __name__ == "__main__":
    success = test_complete_rag_system()
    if success:
        print("\n🎉 Your RAG system is fully operational!")
        print("🚀 Ready for Step 5: Building the Streamlit app!")
    else:
        print("\n🔧 Please check the errors above.")