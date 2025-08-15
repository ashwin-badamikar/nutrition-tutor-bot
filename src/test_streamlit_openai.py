"""
Test Streamlit app with OpenAI integration
Save as src/test_streamlit_openai.py
"""

import streamlit as st
import sys
import os
from pathlib import Path
from dotenv import load_dotenv
import openai

# Load environment variables from project root
project_root = Path(__file__).parent.parent
env_path = project_root / '.env'
load_dotenv(env_path)

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

st.set_page_config(page_title="🧪 OpenAI Test", page_icon="🧪")

st.title("🧪 OpenAI Integration Test")

# Display environment info
st.write("### Environment Check")
st.write(f"**Project root:** {project_root}")
st.write(f"**.env path:** {env_path}")
st.write(f"**.env exists:** {env_path.exists()}")

# Check API key
api_key = os.getenv('OPENAI_API_KEY')
if api_key:
    st.success(f"✅ API Key found: {api_key[:10]}...{api_key[-4:]}")
    
    # Test query
    test_query = st.text_input("Test query:", "What is protein?")
    
    if st.button("🚀 Test OpenAI"):
        try:
            with st.spinner("Testing OpenAI..."):
                openai.api_key = api_key
                
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": test_query}],
                    max_tokens=100
                )
                
                st.success("✅ OpenAI API working!")
                st.write("**Response:**")
                st.write(response.choices[0].message.content)
                
        except Exception as e:
            st.error(f"❌ Error: {e}")
            
    # Test RAG system
    st.write("### RAG System Test")
    if st.button("🔍 Test Vector Search"):
        try:
            from models.vector_store import VectorStoreManager
            
            vs = VectorStoreManager(use_local_embeddings=True)
            results = vs.similarity_search("protein foods", n_results=3)
            
            st.success(f"✅ Found {len(results)} results")
            for i, result in enumerate(results, 1):
                st.write(f"**{i}.** {result['metadata'].get('food_name', 'Unknown')} (similarity: {result['similarity']:.3f})")
                
        except Exception as e:
            st.error(f"❌ Vector search error: {e}")
            
    # Test full RAG
    if st.button("🤖 Test Full RAG"):
        try:
            from models.rag_engine import RAGQueryEngine
            
            rag = RAGQueryEngine(use_local_embeddings=True)
            response = rag.generate_response(
                "What are good protein sources?", 
                response_style="brief"
            )
            
            if "error" not in response:
                st.success("✅ Full RAG working!")
                st.write("**AI Response:**")
                st.write(response["response"])
                st.write(f"**Sources used:** {len(response.get('sources', []))}")
            else:
                st.error(f"❌ RAG error: {response.get('error')}")
                
        except Exception as e:
            st.error(f"❌ RAG system error: {e}")
            
else:
    st.error("❌ No OpenAI API key found")

st.write("---")
st.write("If this works, your main app should work too!")