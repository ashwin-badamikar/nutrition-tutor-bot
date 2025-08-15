"""
Pytest configuration and shared fixtures
Handles path setup and common test utilities
"""

import pytest
import sys
import os
from pathlib import Path
from dotenv import load_dotenv

# Setup paths for testing
project_root = Path(__file__).parent.parent
src_path = project_root / 'src'
env_path = project_root / '.env'

# Add src to Python path
sys.path.insert(0, str(src_path))

# Load environment variables
load_dotenv(env_path)

# Change working directory to src for database access
os.chdir(src_path)

@pytest.fixture(scope="session")
def project_paths():
    """Provide project paths for tests"""
    return {
        'project_root': project_root,
        'src_path': src_path,
        'data_path': project_root / 'data',
        'env_path': env_path
    }

@pytest.fixture(scope="session")  
def ensure_database():
    """Ensure the nutrition database is available for testing"""
    try:
        from models.vector_store import VectorStoreManager
        
        vs = VectorStoreManager(use_local_embeddings=True)
        stats = vs.get_collection_stats()
        
        if stats.get('total_documents', 0) == 0:
            print("🔄 Initializing database for tests...")
            success = vs.load_and_embed_documents()
            if not success:
                pytest.skip("Could not initialize nutrition database for testing")
        
        return vs
        
    except Exception as e:
        pytest.skip(f"Database not available for testing: {e}")

@pytest.fixture
def sample_user_profile():
    """Provide sample user profile for testing"""
    return {
        "age": 25,
        "gender": "Male", 
        "activity_level": "Moderately Active",
        "goals": "Muscle Building",
        "dietary_restrictions": "",
        "preferences": "High Protein"
    }

@pytest.fixture
def nutrition_test_queries():
    """Provide standard test queries for nutrition testing"""
    return [
        {
            "query": "What are good protein sources?",
            "expected_keywords": ["protein", "chicken", "fish", "eggs"],
            "category": "protein"
        },
        {
            "query": "Foods high in vitamin C",
            "expected_keywords": ["vitamin C", "citrus", "orange", "broccoli"],
            "category": "vitamins"
        },
        {
            "query": "Weight loss meal planning",
            "expected_keywords": ["weight loss", "calories", "deficit", "meal"],
            "category": "weight_management"
        }
    ]