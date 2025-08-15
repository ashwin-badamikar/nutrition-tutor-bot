"""
Database Initialization Script
Run this to setup the nutrition database for Streamlit app
Save as src/init_database.py
"""

import sys
from pathlib import Path
import logging

# Setup paths
sys.path.append(str(Path(__file__).parent))

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_nutrition_database():
    """Initialize the complete nutrition database"""
    print("🚀 Initializing Nutrition Tutor Bot Database...")
    print("=" * 50)
    
    # Step 1: Create comprehensive nutrition data
    print("\n1️⃣ Creating nutrition data...")
    try:
        from data.nutrition_data_collector import NutritionDataCollector
        
        collector = NutritionDataCollector()
        food_df = collector.create_comprehensive_food_database()
        knowledge = collector.create_comprehensive_knowledge_base()
        
        print(f"   ✅ Created {len(food_df)} foods")
        print(f"   ✅ Created {len(knowledge)} knowledge entries")
        
    except Exception as e:
        print(f"   ❌ Error creating data: {e}")
        return False
    
    # Step 2: Process data for RAG
    print("\n2️⃣ Processing data for RAG system...")
    try:
        from data.knowledge_processor import KnowledgeProcessor
        
        processor = KnowledgeProcessor()
        documents = processor.create_enhanced_searchable_documents()
        
        print(f"   ✅ Created {len(documents)} searchable documents")
        
    except Exception as e:
        print(f"   ❌ Error processing data: {e}")
        return False
    
    # Step 3: Create vector database
    print("\n3️⃣ Creating vector database...")
    try:
        from models.vector_store import VectorStoreManager
        
        vs = VectorStoreManager(use_local_embeddings=True)
        success = vs.load_and_embed_documents()
        
        if success:
            stats = vs.get_collection_stats()
            print(f"   ✅ Vector database ready!")
            print(f"   📊 Total documents: {stats.get('total_documents', 0)}")
            print(f"   🧠 Embedding model: {stats.get('embedding_model', 'Unknown')}")
            
            # Test search
            results = vs.similarity_search("protein foods", n_results=3)
            print(f"   🔍 Test search: Found {len(results)} relevant results")
            
        else:
            print("   ❌ Vector database creation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Error creating vector database: {e}")
        return False
    
    print("\n🎉 Database initialization complete!")
    print("🚀 You can now run: streamlit run app.py")
    return True

if __name__ == "__main__":
    success = initialize_nutrition_database()
    
    if success:
        print("\n" + "="*50)
        print("✅ SUCCESS: Your Nutrition Tutor Bot is ready!")
        print("📚 Database contains comprehensive nutrition information")
        print("🤖 RAG system is configured and working")
        print("🎯 Run 'streamlit run app.py' to start the application")
        print("="*50)
    else:
        print("\n❌ FAILED: Please fix the errors above and try again")