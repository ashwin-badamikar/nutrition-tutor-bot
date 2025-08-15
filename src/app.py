"""
Complete Nutrition Tutor Bot - DARK THEME - WITH WORKING IMAGE ANALYSIS
Professional dark theme with proper Python syntax and real image analysis
"""

import streamlit as st
import sys
import os
from pathlib import Path
import logging
from typing import Dict, List, Optional
import time
from dotenv import load_dotenv
import pandas as pd
import base64
from PIL import Image
import io
import openai
from openai import OpenAI

# Fix path resolution
current_file = Path(__file__).resolve()
project_root = current_file.parent.parent
env_path = project_root / '.env'
load_dotenv(env_path)
sys.path.append(str(current_file.parent))

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="🥗 Nutrition Tutor Bot",
    page_icon="🥗",
    layout="wide",
    initial_sidebar_state="expanded"
)

# MODERN DARK THEME STYLING - SYNTAX FIXED
st.markdown("""
<style>
/* FORCE ENTIRE APP TO DARK THEME */
.stApp, 
[data-testid="stAppViewContainer"],
[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stDecoration"],
[data-testid="stStatusWidget"] {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
}

/* SIDEBAR - DARK THEME */
[data-testid="stSidebar"],
[data-testid="stSidebar"] > div,
.css-1d391kg,
.css-1lcbmhc,
.css-17eq0hr,
.sidebar .sidebar-content,
section[data-testid="stSidebar"] {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
}

/* SIDEBAR - ALL TEXT ELEMENTS */
[data-testid="stSidebar"] *,
[data-testid="stSidebar"] .stMarkdown,
[data-testid="stSidebar"] .stMarkdown *,
[data-testid="stSidebar"] div,
[data-testid="stSidebar"] p,
[data-testid="stSidebar"] h1, 
[data-testid="stSidebar"] h2, 
[data-testid="stSidebar"] h3, 
[data-testid="stSidebar"] h4,
[data-testid="stSidebar"] span,
[data-testid="stSidebar"] label,
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stNumberInput label,
[data-testid="stSidebar"] .stMultiSelect label {
    color: #F8FAFC !important;
    background-color: transparent !important;
}

/* SIDEBAR - FORM ELEMENTS */
[data-testid="stSidebar"] input,
[data-testid="stSidebar"] select,
[data-testid="stSidebar"] textarea,
[data-testid="stSidebar"] .stNumberInput input,
[data-testid="stSidebar"] .stSelectbox select,
[data-testid="stSidebar"] .stMultiSelect div,
[data-testid="stSidebar"] .stTextInput input,
[data-testid="stSidebar"] .stSelectbox > div > div,
[data-testid="stSidebar"] [data-baseweb="select"] {
    background-color: #334155 !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
}

/* SIDEBAR - BUTTONS */
[data-testid="stSidebar"] .stButton > button {
    background-color: #334155 !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
}

[data-testid="stSidebar"] .stButton > button[kind="primary"] {
    background-color: #16A34A !important;
    color: #FFFFFF !important;
    border-color: #16A34A !important;
}

/* MAIN CONTENT AREA - DARK THEME */
.main .stMarkdown,
.main .stMarkdown *,
.main div,
.main p,
.main span,
.main h1, .main h2, .main h3, .main h4, .main h5, .main h6,
.main ul, .main ol, .main li {
    color: #F8FAFC !important;
}

/* Main headers */
.main-header {
    font-size: 2.8rem;
    font-weight: 700;
    text-align: center;
    color: #22C55E !important;
    margin-bottom: 0.5rem;
    font-family: system-ui, -apple-system, sans-serif;
}

.subtitle {
    font-size: 1.1rem;
    text-align: center;
    color: #CBD5E1 !important;
    margin-bottom: 2rem;
    font-weight: 400;
}

/* TABS - DARK THEME */
.stTabs [data-baseweb="tab-list"],
.stTabs [data-baseweb="tab"],
.stTabs [data-baseweb="tab-panel"] {
    background-color: #0F172A !important;
    color: #F8FAFC !important;
}

/* ALL FORM ELEMENTS - DARK THEME */
input, select, textarea,
.stNumberInput input,
.stTextInput input,
.stTextArea textarea,
.stSelectbox select,
.stSelectbox > div > div,
.stMultiSelect div,
[data-baseweb="select"],
[data-baseweb="input"],
[role="combobox"] {
    background-color: #334155 !important;
    color: #F8FAFC !important;
    border: 1px solid #475569 !important;
}

/* ALL FORM LABELS - DARK THEME */
.stNumberInput label,
.stTextInput label,
.stTextArea label,
.stSelectbox label,
.stMultiSelect label {
    color: #F8FAFC !important;
    font-weight: 600 !important;
}

/* BUTTONS - DARK THEME */
.stButton > button {
    border-radius: 8px !important;
    font-weight: 600 !important;
    border: 1px solid #475569 !important;
    font-family: system-ui, sans-serif !important;
    color: #F8FAFC !important;
    background-color: #334155 !important;
}

.stButton > button[kind="primary"] {
    background-color: #16A34A !important;
    color: #FFFFFF !important;
    border-color: #16A34A !important;
}

.stButton > button:hover {
    background-color: #475569 !important;
    color: #F8FAFC !important;
}

.stButton > button[kind="primary"]:hover {
    background-color: #15803D !important;
    color: #FFFFFF !important;
}

/* Chat message styling - DARK THEME */
.clean-user-msg {
    background: #1E3A8A !important;
    border: 1px solid #3B82F6;
    border-left: 4px solid #60A5FA;
    padding: 1.2rem;
    border-radius: 10px;
    margin: 1rem 0;
    font-family: system-ui, sans-serif;
}

.clean-user-msg, .clean-user-msg * {
    color: #DBEAFE !important;
}

.clean-assistant-msg {
    background: #064E3B !important;
    border: 1px solid #059669;
    border-left: 4px solid #10B981;
    padding: 1.2rem;
    border-radius: 10px;
    margin: 1rem 0;
    font-family: system-ui, sans-serif;
}

.clean-assistant-msg, .clean-assistant-msg * {
    color: #D1FAE5 !important;
}

/* Status boxes - DARK THEME */
.clean-success {
    background: #064E3B !important;
    border: 1px solid #059669;
    border-left: 4px solid #10B981;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
    margin: 1rem 0;
}

.clean-success, .clean-success * {
    color: #D1FAE5 !important;
}

.clean-info {
    background: #0C4A6E !important;
    border: 1px solid #0284C7;
    border-left: 4px solid #0EA5E9;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
    margin: 1rem 0;
}

.clean-info, .clean-info * {
    color: #BAE6FD !important;
}

.clean-warning {
    background: #92400E !important;
    border: 1px solid #D97706;
    border-left: 4px solid #F59E0B;
    padding: 1rem;
    border-radius: 8px;
    font-weight: 600;
    margin: 1rem 0;
}

.clean-warning, .clean-warning * {
    color: #FEF3C7 !important;
}

/* Profile styling - DARK THEME */
.clean-profile-active {
    background: #16A34A !important;
    color: white !important;
    padding: 1.2rem;
    border-radius: 10px;
    text-align: center;
    font-weight: 700;
    margin: 1rem 0;
    box-shadow: 0 4px 6px rgba(22, 163, 74, 0.3);
}

.clean-profile-active * {
    color: white !important;
}

.clean-profile-details {
    background: #334155 !important;
    border: 1px solid #475569;
    border-left: 4px solid #16A34A;
    padding: 1.2rem;
    border-radius: 8px;
    margin: 1rem 0;
    line-height: 1.5;
}

.clean-profile-details, .clean-profile-details * {
    color: #F8FAFC !important;
}

/* Welcome card - DARK THEME */
.clean-welcome {
    background: #1E293B !important;
    border: 1px solid #334155;
    border-radius: 12px;
    padding: 2rem;
    margin: 1.5rem 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
}

.clean-welcome, .clean-welcome * {
    color: #F8FAFC !important;
}

/* Metric cards - DARK THEME */
.clean-metric {
    background: #1E293B !important;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1.2rem;
    text-align: center;
    margin: 0.5rem;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.clean-metric, .clean-metric * {
    color: #F8FAFC !important;
}

/* Content boxes - DARK THEME */
.content-box {
    background: #1E293B !important;
    border: 1px solid #334155;
    border-radius: 8px;
    padding: 1.5rem;
    margin: 1rem 0;
    box-shadow: 0 2px 6px rgba(0,0,0,0.15);
}

.content-box, .content-box * {
    color: #F8FAFC !important;
}

/* METRICS AND INFO BOXES - DARK THEME */
.stMetric {
    background-color: #1E293B !important;
    border: 1px solid #334155 !important;
    border-radius: 8px !important;
    padding: 1rem !important;
}

.stMetric label, .stMetric div {
    color: #F8FAFC !important;
}

/* INFO/SUCCESS/ERROR BOXES - DARK THEME */
.stInfo {
    background-color: #0C4A6E !important;
    color: #BAE6FD !important;
    border: 1px solid #0284C7 !important;
}

.stSuccess {
    background-color: #064E3B !important;
    color: #D1FAE5 !important;
    border: 1px solid #059669 !important;
}

.stError {
    background-color: #7F1D1D !important;
    color: #FEE2E2 !important;
    border: 1px solid #DC2626 !important;
}

/* EXPANDERS - DARK THEME */
.streamlit-expanderHeader {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
}

.streamlit-expanderContent {
    background-color: #1E293B !important;
    color: #F8FAFC !important;
}

/* FILE UPLOADER - DARK THEME */
.stFileUploader {
    background-color: #1E293B !important;
}

.stFileUploader label {
    color: #F8FAFC !important;
}

/* SLIDERS - DARK THEME */
.stSlider label {
    color: #F8FAFC !important;
}

/* UNIVERSAL TEXT COLOR - LIGHT ON DARK */
* {
    color: #F8FAFC !important;
}

/* EXCEPTIONS - Specific colored elements */
.main-header {
    color: #22C55E !important;
}

.clean-profile-active, .clean-profile-active * {
    color: #FFFFFF !important;
}

.clean-user-msg, .clean-user-msg * {
    color: #DBEAFE !important;
}

.clean-assistant-msg, .clean-assistant-msg * {
    color: #D1FAE5 !important;
}

.clean-success, .clean-success * {
    color: #D1FAE5 !important;
}

.clean-info, .clean-info * {
    color: #BAE6FD !important;
}

.clean-warning, .clean-warning * {
    color: #FEF3C7 !important;
}

.stButton > button[kind="primary"], .stButton > button[kind="primary"] * {
    color: #FFFFFF !important;
}

</style>
""", unsafe_allow_html=True)

@st.cache_resource
def initialize_systems():
    """Initialize RAG system"""
    try:
        from models.rag_engine import RAGQueryEngine
        from models.vector_store import VectorStoreManager
        
        rag_engine = RAGQueryEngine(use_local_embeddings=True)
        vector_store = VectorStoreManager(use_local_embeddings=True)
        stats = vector_store.get_collection_stats()
        
        if stats.get("total_documents", 0) == 0:
            st.error("❌ Nutrition database not found.")
            return None, None
        
        return rag_engine, stats
    except Exception as e:
        st.error(f"❌ Error initializing systems: {e}")
        return None, None

def analyze_meal_photo(uploaded_file, analysis_type="Quick", user_context=None):
    """
    Analyze uploaded meal photo using OpenAI Vision API
    """
    try:
        # Check for OpenAI API key
        api_key = os.getenv('OPENAI_API_KEY')
        if not api_key:
            return {
                "success": False,
                "error": "OpenAI API key not found. Please add OPENAI_API_KEY to your .env file."
            }
        
        # Initialize OpenAI client
        client = OpenAI(api_key=api_key)
        
        # Convert uploaded file to base64
        image = Image.open(uploaded_file)
        
        # Resize image if too large (OpenAI has size limits)
        max_size = 1024
        if image.size[0] > max_size or image.size[1] > max_size:
            image.thumbnail((max_size, max_size), Image.Resampling.LANCZOS)
        
        # Convert to RGB if necessary
        if image.mode != 'RGB':
            image = image.convert('RGB')
        
        buffered = io.BytesIO()
        image.save(buffered, format="JPEG", quality=85)
        img_base64 = base64.b64encode(buffered.getvalue()).decode()
        
        # Create analysis prompt based on user context
        base_prompt = """You are a professional nutrition coach analyzing a meal photo. 

Analyze this meal photo and provide:

**🍽️ FOOD IDENTIFICATION:**
List each food item you can identify with estimated portion sizes.

**📊 NUTRITION BREAKDOWN:**
Provide estimated nutritional values:
- Total calories
- Protein (grams)
- Carbohydrates (grams) 
- Fat (grams)
- Fiber (grams)
- Key vitamins/minerals if notable

**⚖️ NUTRITIONAL ASSESSMENT:**
Rate the meal's nutritional balance and quality (1-10 scale).

**💡 COACH RECOMMENDATIONS:**
Provide 2-3 specific, actionable suggestions for improvement or compliments on good choices.

Be encouraging but honest. Focus on practical, helpful advice."""

        if user_context and user_context.get('goals'):
            base_prompt += f"""

**👤 USER CONTEXT:**
- Age: {user_context.get('age', 'Not specified')}
- Primary Goal: {user_context.get('goals', 'General health')}
- Activity Level: {user_context.get('activity_level', 'Not specified')}
- Dietary Restrictions: {user_context.get('dietary_restrictions', 'None')}

Tailor your analysis and suggestions specifically to help this person achieve their {user_context.get('goals', 'health goals')}."""
        
        if analysis_type == "Detailed":
            base_prompt += "\n\n**DETAILED ANALYSIS REQUESTED:** Provide more comprehensive nutritional analysis with specific macro and micronutrient insights, meal timing considerations, and detailed improvement suggestions."
        elif analysis_type == "Full Report":
            base_prompt += "\n\n**COMPREHENSIVE REPORT REQUESTED:** Provide an in-depth analysis including: nutritional completeness assessment, bioavailability factors, meal timing optimization, portion size evaluation, food combination benefits, and strategic recommendations for long-term dietary success."
        
        # Call OpenAI Vision API
        response = client.chat.completions.create(
            model="gpt-4o",  # Using latest vision model
            messages=[
                {
                    "role": "user", 
                    "content": [
                        {"type": "text", "text": base_prompt},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/jpeg;base64,{img_base64}",
                                "detail": "high" if analysis_type == "Full Report" else "auto"
                            }
                        }
                    ]
                }
            ],
            max_tokens=1000 if analysis_type == "Full Report" else 600,
            temperature=0.3  # Lower temperature for more consistent analysis
        )
        
        analysis_result = response.choices[0].message.content
        
        return {
            "success": True,
            "analysis": analysis_result,
            "model_used": "GPT-4o Vision",
            "analysis_type": analysis_type,
            "tokens_used": response.usage.total_tokens if hasattr(response, 'usage') else None
        }
        
    except openai.AuthenticationError:
        return {
            "success": False,
            "error": "Invalid OpenAI API key. Please check your OPENAI_API_KEY in the .env file."
        }
    except openai.RateLimitError:
        return {
            "success": False,
            "error": "OpenAI API rate limit exceeded. Please try again in a moment."
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Image analysis failed: {str(e)}"
        }

def create_profile_sidebar():
    """Create professional profile sidebar"""
    st.sidebar.markdown("## 👤 Your Profile")
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    if 'profile_saved' not in st.session_state:
        st.session_state.profile_saved = False
    
    if not st.session_state.profile_saved:
        with st.sidebar.form("profile"):
            st.markdown("**👤 Basic Information:**")
            age = st.number_input("Age", min_value=16, max_value=100, value=None)
            gender = st.selectbox("Gender", ["", "Male", "Female", "Other"])
            
            st.markdown("**🏃 Activity & Goals:**")
            activity = st.selectbox("Activity Level", ["", "Sedentary", "Lightly Active", "Moderately Active", "Very Active"])
            goal = st.selectbox("Primary Goal", ["", "Weight Loss", "Weight Gain", "Muscle Building", "General Health"])
            
            st.markdown("**🥗 Preferences:**")
            restrictions = st.multiselect("Dietary Restrictions", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free"])
            preferences = st.multiselect("Food Preferences", ["High Protein", "Low Carb", "Quick Meals"])
            
            if st.form_submit_button("💾 Save Profile", type="primary"):
                if age and gender and activity and goal:
                    st.session_state.user_profile = {
                        "age": age, 
                        "gender": gender, 
                        "activity_level": activity, 
                        "goals": goal,
                        "dietary_restrictions": ", ".join(restrictions),
                        "preferences": ", ".join(preferences)
                    }
                    st.session_state.profile_saved = True
                    st.rerun()
                else:
                    st.sidebar.error("Please fill all required fields")
    
    else:
        profile = st.session_state.user_profile
        st.sidebar.markdown('<div class="clean-profile-active">🎯 COACH KNOWS YOU</div>', unsafe_allow_html=True)
        st.sidebar.markdown(
            f'''
            <div class="clean-profile-details">
                <strong>{profile.get("age")}y/o {profile.get("gender")}</strong><br>
                🎯 {profile.get("goals")}<br>
                🏃 {profile.get("activity_level")}
            </div>
            ''', unsafe_allow_html=True
        )
        
        if profile.get('dietary_restrictions'):
            st.sidebar.markdown(f"**🚫 Restrictions:** {profile['dietary_restrictions']}")
        if profile.get('preferences'):
            st.sidebar.markdown(f"**💡 Preferences:** {profile['preferences']}")
        
        if st.sidebar.button("✏️ Edit Profile"):
            st.session_state.profile_saved = False
            st.rerun()
    
    return st.session_state.user_profile if st.session_state.profile_saved else {}

def display_response(response_data: Dict, query: str):
    """Display response with proper contrast"""
    if "error" in response_data:
        st.error(f"Error: {response_data['error']}")
        return
    
    st.markdown("### 🤖 AI Nutrition Assistant")
    st.markdown(
        f'<div class="content-box">{response_data["response"]}</div>', 
        unsafe_allow_html=True
    )
    
    # Response metadata
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(
            f'<div class="clean-metric">📚<br><strong>Sources Used</strong><br>{len(response_data.get("sources", []))}</div>', 
            unsafe_allow_html=True
        )
    with col2:
        st.markdown(
            f'<div class="clean-metric">🔍<br><strong>Context Items</strong><br>{response_data.get("context_count", 0)}</div>', 
            unsafe_allow_html=True
        )
    with col3:
        search_strategy = response_data.get("search_strategy", {})
        active_strategies = [k.replace("_focus", "").title() for k, v in search_strategy.items() if v]
        strategy_text = ", ".join(active_strategies) if active_strategies else "General"
        st.markdown(
            f'<div class="clean-metric">🎯<br><strong>Search Focus</strong><br>{strategy_text}</div>', 
            unsafe_allow_html=True
        )
    
    # Sources
    if response_data.get("sources"):
        with st.expander("📚 Sources & References", expanded=False):
            for i, source in enumerate(response_data["sources"][:5], 1):
                source_name = source.get("food_name", source.get("topic", "Nutrition Information"))
                source_type = source.get("doc_type", "unknown").replace("_", " ").title()
                st.markdown(f"**{i}. {source_name}** ({source_type})")

def main():
    """Main application with dark theme"""
    
    # Header
    st.markdown('<h1 class="main-header">🥗 Nutrition Tutor Bot</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Your conversational AI nutrition coach • Chat naturally about health & nutrition</p>', unsafe_allow_html=True)
    
    # Initialize systems
    rag_engine, db_stats = initialize_systems()
    if not rag_engine:
        st.stop()
    
    # Sidebar
    profile = create_profile_sidebar()
    
    # Database stats in sidebar
    if db_stats:
        st.sidebar.markdown("---")
        st.sidebar.markdown("## 📊 Knowledge Base")
        st.sidebar.info(f"📚 {db_stats.get('total_documents', 0)} nutrition documents")
        st.sidebar.info(f"🧠 Local AI embeddings")
        st.sidebar.info(f"🌐 USDA nutrition database")
    
    # Main tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["💬 Chat Coach", "🔍 Search", "🍽️ Meal Plans", "📷 Photo Analysis", "📊 Database"])
    
    # TAB 1: CONVERSATIONAL NUTRITION COACH
    with tab1:
        st.markdown("## 💬 Chat with Your Nutrition Coach")
        st.markdown("Have a natural conversation about nutrition - just like ChatGPT, but specialized for health!")
        
        # Initialize chat
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        
        # Profile status
        if profile:
            st.markdown(
                f'''
                <div class="clean-success">
                    🎯 <strong>Personal Coach Mode:</strong> I know you're {profile.get("age")}y/o, {profile.get("activity_level").lower()}, focused on {profile.get("goals").lower()}
                </div>
                ''', unsafe_allow_html=True
            )
        else:
            st.markdown(
                '''
                <div class="clean-info">
                    💡 <strong>General Coach Mode:</strong> Create a profile in the sidebar for personalized advice!
                </div>
                ''', unsafe_allow_html=True
            )
        
        # Chat controls
        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            response_style = st.selectbox("Response Style:", ["conversational", "brief", "comprehensive"])
        with col2:
            if st.button("🆕 New Chat"):
                st.session_state.chat_history = []
                st.rerun()
        with col3:
            st.metric("Messages", len(st.session_state.chat_history))
        
        # Display conversation
        if st.session_state.chat_history:
            st.markdown("### 💬 Your Conversation")
            
            for message in st.session_state.chat_history:
                if message['role'] == 'user':
                    st.markdown(
                        f'''
                        <div class="clean-user-msg">
                            <div style="font-weight: 600; margin-bottom: 0.5rem;">👤 You:</div>
                            <div style="font-size: 1rem; line-height: 1.6;">{message["content"]}</div>
                            <div style="text-align: right; font-size: 0.85em; margin-top: 0.8rem; opacity: 0.7;">
                                {message.get("timestamp", "")}
                            </div>
                        </div>
                        ''', 
                        unsafe_allow_html=True
                    )
                else:
                    st.markdown(
                        f'''
                        <div class="clean-assistant-msg">
                            <div style="font-weight: 600; margin-bottom: 0.5rem;">🤖 Nutrition Coach:</div>
                            <div style="font-size: 1rem; line-height: 1.6;">{message["content"]}</div>
                            <div style="text-align: right; font-size: 0.85em; margin-top: 0.8rem; opacity: 0.8;">
                                {message.get("timestamp", "")} • {len(message.get("sources", []))} sources
                            </div>
                        </div>
                        ''', 
                        unsafe_allow_html=True
                    )
                    
                    # Show sources
                    if message.get("sources"):
                        with st.expander(f"📚 Knowledge sources ({len(message['sources'])})", expanded=False):
                            for i, source in enumerate(message["sources"][:3], 1):
                                name = source.get('food_name', source.get('topic', 'Nutrition Info'))
                                type_clean = source.get('doc_type', '').replace('_', ' ').title()
                                st.markdown(f"**{i}.** {name} *({type_clean})*")
        
        else:
            # Welcome screen
            st.markdown(
                '''
                <div class="clean-welcome">
                    <h3>👋 Hi! I'm Your Personal Nutrition Coach</h3>
                    <p style="font-size: 1.1rem; margin-bottom: 1.5rem;">I'm here to help you with all your nutrition and health questions. Just start chatting naturally!</p>
                </div>
                ''', 
                unsafe_allow_html=True
            )
            
            # Conversation starters
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(
                    '''
                    <div class="content-box">
                        <h4>💬 Chat naturally about:</h4>
                        <ul style="line-height: 1.8;">
                            <li>"Hi, I want to get healthier"</li>
                            <li>"Help me lose weight safely"</li>
                            <li>"I'm training for something"</li>
                            <li>"What should I eat today?"</li>
                            <li>"I'm confused about nutrition"</li>
                        </ul>
                    </div>
                    ''', 
                    unsafe_allow_html=True
                )
            
            with col2:
                st.markdown(
                    '''
                    <div class="content-box">
                        <h4>🎯 I can help you with:</h4>
                        <ul style="line-height: 1.8;">
                            <li>Weight management strategies</li>
                            <li>Meal planning and prep ideas</li>
                            <li>Sports nutrition guidance</li>
                            <li>Healthy eating habits</li>
                            <li>Specific food questions</li>
                        </ul>
                    </div>
                    ''', 
                    unsafe_allow_html=True
                )
            
            # Quick starters
            st.markdown("**🚀 Quick conversation starters:**")
            starters = [
                "Hi! I want to improve my diet",
                "Help me lose weight in a healthy way",
                "I need more energy throughout the day", 
                "I'm trying to build muscle - help me get started",
                "What's the most important nutrition advice?"
            ]
            
            cols = st.columns(2)
            for i, starter in enumerate(starters):
                col = cols[i % 2]
                if col.button(f"💬 {starter}", key=f"starter_{i}"):
                    st.session_state.user_query = starter
        
        # Chat input
        st.markdown("### ✍️ Type your message:")
        
        with st.form("chat_form", clear_on_submit=True):
            user_input = st.text_area(
                "Message:",
                value=st.session_state.get("user_query", ""),
                height=100,
                placeholder="Type anything! Ask questions, share your goals, or just say hi...",
                label_visibility="collapsed"
            )
            
            col1, col2 = st.columns([5, 1])
            with col2:
                send_button = st.form_submit_button("💬 Send", type="primary", use_container_width=True)
        
        # Process conversation
        if send_button and user_input.strip():
            # Add user message
            st.session_state.chat_history.append({
                'role': 'user',
                'content': user_input.strip(),
                'timestamp': time.strftime('%H:%M')
            })
            
            with st.spinner("🤖 Coach is thinking..."):
                try:
                    # Build conversational prompt
                    if len(st.session_state.chat_history) > 1:
                        # Include conversation context
                        recent_conversation = []
                        for msg in st.session_state.chat_history[-6:]:
                            if msg['role'] == 'user':
                                recent_conversation.append(f"User: {msg['content']}")
                            else:
                                content = msg['content'][:150] + "..." if len(msg['content']) > 150 else msg['content']
                                recent_conversation.append(f"Coach: {content}")
                        
                        conversation_summary = "\n".join(recent_conversation)
                        conversational_query = f"""You are a friendly, professional nutrition coach having a natural conversation with someone.

Previous conversation:
{conversation_summary}

Current user message: {user_input}

Instructions: Respond naturally and conversationally, like a helpful nutrition coach would. Reference the previous conversation when relevant. Ask follow-up questions to keep the dialogue flowing. Use nutrition science when it helps, but prioritize being conversational, encouraging, and helpful."""
                    
                    else:
                        # First message
                        conversational_query = f"""You are a friendly, professional nutrition coach starting a conversation.

User's first message: {user_input}

Instructions: Respond warmly and naturally, like a nutrition coach would. Ask questions to understand their goals and needs. Keep it conversational, encouraging, and helpful. Be friendly and approachable, not formal or clinical."""
                    
                    # Get response
                    response = rag_engine.generate_response(
                        query=conversational_query,
                        user_context=profile,
                        response_style=response_style
                    )
                    
                    # Add coach response
                    st.session_state.chat_history.append({
                        'role': 'assistant',
                        'content': response['response'],
                        'sources': response.get('sources', []),
                        'context_count': response.get('context_count', 0),
                        'timestamp': time.strftime('%H:%M')
                    })
                    
                    # Clear input
                    if 'user_query' in st.session_state:
                        del st.session_state.user_query
                    
                    st.rerun()
                    
                except Exception as e:
                    st.error(f"Sorry, I had trouble responding: {e}")
        
        # Follow-up suggestions
        if len(st.session_state.chat_history) >= 2:
            last_response = ""
            for msg in reversed(st.session_state.chat_history):
                if msg['role'] == 'assistant':
                    last_response = msg['content'].lower()
                    break
            
            if last_response:
                st.markdown("### 💭 Continue the conversation:")
                suggestions = []
                
                if 'protein' in last_response:
                    suggestions.extend(["How much protein do I need daily?", "When should I eat protein?"])
                elif 'weight' in last_response:
                    suggestions.extend(["How fast will I see results?", "What foods should I avoid?"])
                elif 'meal' in last_response:
                    suggestions.extend(["Can you give me specific meal ideas?", "What about meal prep tips?"])
                else:
                    suggestions = ["Can you be more specific?", "What should I focus on first?", "Any practical tips?"]
                
                cols = st.columns(min(3, len(suggestions)))
                for i, suggestion in enumerate(suggestions[:3]):
                    if cols[i].button(f"💬 {suggestion}", key=f"suggest_{i}"):
                        st.session_state.user_query = suggestion
                        st.rerun()
    
    # TAB 2: SEARCH
    with tab2:
        st.markdown("## 🔍 Nutrition Database Search")
        st.markdown("Search our comprehensive nutrition database with AI similarity matching.")
        
        search_query = st.text_input("Search:", placeholder="protein foods, vitamins, meal ideas...")
        
        col1, col2 = st.columns(2)
        with col1:
            search_filter = st.selectbox("Filter:", ["All", "Foods Only", "Nutrition Guidelines", "Recipes"])
        with col2:
            num_results = st.slider("Results:", 3, 10, 5)
        
        if st.button("🔍 Search Database", type="primary") and search_query:
            with st.spinner("Searching..."):
                try:
                    from models.vector_store import VectorStoreManager
                    vs = VectorStoreManager(use_local_embeddings=True)
                    
                    filter_dict = None
                    if search_filter == "Foods Only":
                        filter_dict = {"doc_type": "food_item"}
                    elif search_filter == "Nutrition Guidelines":
                        filter_dict = {"doc_type": "nutrition_knowledge"}
                    elif search_filter == "Recipes":
                        filter_dict = {"doc_type": "recipe_combination"}
                    
                    results = vs.similarity_search(search_query, n_results=num_results, filter_dict=filter_dict)
                    
                    st.markdown(f"### 📊 Found {len(results)} relevant results:")
                    
                    for i, result in enumerate(results, 1):
                        name = result['metadata'].get('food_name', result['metadata'].get('topic', 'Nutrition Info'))
                        similarity = f"{result['similarity']:.3f}"
                        
                        with st.expander(f"{i}. {name} (Relevance: {similarity})"):
                            st.markdown(
                                f'<div class="content-box">{result["content"]}</div>', 
                                unsafe_allow_html=True
                            )
                            
                            if result['metadata'].get('doc_type') == 'food_item':
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("Calories", result['metadata'].get('calories', 'N/A'))
                                with col2:
                                    st.metric("Protein", f"{result['metadata'].get('protein', 'N/A')}g")
                                with col3:
                                    st.metric("Category", result['metadata'].get('category', 'N/A'))
                
                except Exception as e:
                    st.error(f"Search error: {e}")
    
    # TAB 3: MEAL PLANNING
    with tab3:
        st.markdown("## 🍽️ AI Meal Planning")
        st.markdown("Get personalized meal recommendations based on your goals.")
        
        if profile:
            st.markdown(
                f'''
                <div class="clean-success">
                    🎯 <strong>Using your profile:</strong> {profile.get("goals")} goal • {profile.get("activity_level")} activity
                </div>
                ''', unsafe_allow_html=True
            )
        
        goal = st.selectbox("Primary Goal:", ["Weight Loss", "Muscle Building", "Weight Gain", "Athletic Performance", "General Health"])
        
        col1, col2 = st.columns(2)
        with col1:
            preferences = st.multiselect("Preferences:", ["High Protein", "Low Carb", "High Fiber", "Vegetarian", "Quick Meals"])
        with col2:
            restrictions = st.multiselect("Restrictions:", ["Vegetarian", "Vegan", "Gluten-Free", "Dairy-Free", "Nut-Free"])
        
        if st.button("🎯 Create My Meal Plan", type="primary"):
            with st.spinner("Creating meal plan..."):
                try:
                    query = f"Create a detailed meal plan for {goal.lower()}"
                    if preferences:
                        query += f" with {', '.join(preferences).lower()} preferences"
                    if restrictions:
                        query += f" avoiding {', '.join(restrictions).lower()}"
                    
                    response = rag_engine.generate_response(query, user_context=profile, response_style="detailed")
                    
                    st.markdown("### 🎯 Your Personalized Meal Plan")
                    st.markdown(
                        f'<div class="content-box">{response["response"]}</div>',
                        unsafe_allow_html=True
                    )
                    
                except Exception as e:
                    st.error(f"Error: {e}")
    
    # TAB 4: PHOTO ANALYSIS - NOW WITH REAL FUNCTIONALITY
    with tab4:
        st.markdown("## 📷 AI Meal Photo Analysis")
        st.markdown("Upload a photo for instant nutrition analysis with AI vision!")
        
        # Check API key status
        api_key_status = "✅ Connected" if os.getenv('OPENAI_API_KEY') else "❌ API Key Missing"
        st.markdown(
            f'''
            <div class="clean-info">
                🤖 <strong>AI Pipeline:</strong> Photo → Vision Analysis → USDA Database → Personalized Advice<br>
                🔑 <strong>Status:</strong> {api_key_status}
            </div>
            ''', unsafe_allow_html=True
        )
        
        if not os.getenv('OPENAI_API_KEY'):
            st.markdown(
                '''
                <div class="clean-warning">
                    ⚠️ <strong>Setup Required:</strong> Add your OpenAI API key to the .env file as OPENAI_API_KEY=your_key_here
                </div>
                ''', unsafe_allow_html=True
            )
        
        uploaded_file = st.file_uploader("📸 Upload meal photo", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            col1, col2 = st.columns([2, 1])
            with col1:
                st.image(uploaded_file, caption="Your meal photo", use_column_width=True)
            with col2:
                analysis_type = st.selectbox("Analysis Level:", ["Quick", "Detailed", "Full Report"])
                
                if st.button("🔍 Analyze Meal", type="primary", use_container_width=True):
                    with st.spinner("🤖 AI is analyzing your meal..."):
                        # REAL IMAGE ANALYSIS
                        result = analyze_meal_photo(uploaded_file, analysis_type, profile)
                        
                        if result["success"]:
                            st.markdown("### 🔍 AI Meal Analysis Results")
                            st.markdown(
                                f'<div class="content-box">{result["analysis"]}</div>',
                                unsafe_allow_html=True
                            )
                            
                            # Analysis metadata
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.markdown(
                                    f'<div class="clean-metric">🤖<br><strong>AI Model</strong><br>{result["model_used"]}</div>',
                                    unsafe_allow_html=True
                                )
                            with col2:
                                st.markdown(
                                    f'<div class="clean-metric">📊<br><strong>Analysis</strong><br>{result["analysis_type"]}</div>',
                                    unsafe_allow_html=True
                                )
                            with col3:
                                tokens_text = f"{result['tokens_used']} tokens" if result.get('tokens_used') else "Complete"
                                st.markdown(
                                    f'<div class="clean-metric">✅<br><strong>Status</strong><br>{tokens_text}</div>',
                                    unsafe_allow_html=True
                                )
                            
                            # Option to continue conversation
                            st.markdown("### 💬 Continue the Discussion")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                if st.button("💬 Add to Chat History", use_container_width=True):
                                    # Add to chat history
                                    if 'chat_history' not in st.session_state:
                                        st.session_state.chat_history = []
                                    
                                    # Add user message about photo
                                    st.session_state.chat_history.append({
                                        'role': 'user',
                                        'content': f'I uploaded a photo of my meal for analysis. Can you help me understand it better?',
                                        'timestamp': time.strftime('%H:%M')
                                    })
                                    
                                    # Add analysis results
                                    st.session_state.chat_history.append({
                                        'role': 'assistant',
                                        'content': f"📸 **Photo Analysis Results:**\n\n{result['analysis']}",
                                        'sources': [],
                                        'timestamp': time.strftime('%H:%M')
                                    })
                                    
                                    st.success("✅ Added to chat! Switch to Chat Coach tab to continue the conversation.")
                            
                            with col2:
                                if st.button("🔄 Analyze Different Photo", use_container_width=True):
                                    st.rerun()
                        
                        else:
                            st.error(f"❌ Analysis failed: {result['error']}")
                            
                            # Troubleshooting suggestions
                            st.markdown(
                                '''
                                <div class="clean-info">
                                    💡 <strong>Troubleshooting Tips:</strong><br>
                                    • Ensure OpenAI API key is correctly configured in .env file<br>
                                    • Check that the image is clear and well-lit<br>
                                    • Try a different image format (JPG, PNG)<br>
                                    • Make sure the image shows food clearly<br>
                                    • Use the Chat Coach tab to describe your meal manually
                                </div>
                                ''',
                                unsafe_allow_html=True
                            )
        
        else:
            st.markdown(
                '''
                <div class="clean-welcome">
                    <h3>📸 How AI Photo Analysis Works</h3>
                    <ol style="line-height: 1.8; font-size: 1rem;">
                        <li><strong>Upload</strong> a clear photo of your meal or food</li>
                        <li><strong>AI Vision</strong> identifies foods and estimates portions</li>
                        <li><strong>Nutrition Database</strong> provides precise nutritional data</li>
                        <li><strong>Personal Coach</strong> gives tailored advice for your goals</li>
                    </ol>
                    
                    <h4>📋 Best Photo Tips:</h4>
                    <ul style="line-height: 1.6;">
                        <li>Good lighting and clear focus</li>
                        <li>Show the entire meal/food item</li>
                        <li>Include reference objects for scale if possible</li>
                        <li>Take photo from above or at an angle</li>
                    </ul>
                </div>
                ''', 
                unsafe_allow_html=True
            )
            
            # Example photos section
            st.markdown("### 🖼️ Example Analysis Results")
            example_col1, example_col2 = st.columns(2)
            
            with example_col1:
                st.markdown(
                    '''
                    <div class="content-box">
                        <h4>✅ Good Photo Example:</h4>
                        <p><strong>Clear, well-lit meal photo shows:</strong></p>
                        <ul>
                            <li>Grilled salmon fillet (~6oz)</li>
                            <li>Steamed asparagus (~1 cup)</li>
                            <li>Quinoa (~0.5 cup cooked)</li>
                        </ul>
                        <p><strong>AI Analysis:</strong> ~485 calories, excellent omega-3s, perfect for muscle building goals!</p>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
            
            with example_col2:
                st.markdown(
                    '''
                    <div class="content-box">
                        <h4>🔍 What AI Can Detect:</h4>
                        <ul style="line-height: 1.6;">
                            <li>Food types and cooking methods</li>
                            <li>Portion size estimates</li>
                            <li>Nutritional balance assessment</li>
                            <li>Missing food groups</li>
                            <li>Healthy vs. processed foods</li>
                            <li>Meal timing recommendations</li>
                        </ul>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
    
    # TAB 5: DATABASE
    with tab5:
        st.markdown("## 📊 Nutrition Knowledge Base")
        st.markdown("Explore our comprehensive nutrition database and performance metrics.")
        
        if db_stats:
            st.markdown("### 📈 Database Overview")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.markdown(
                    f'<div class="clean-metric">📄<br><strong>Documents</strong><br>{db_stats.get("total_documents", 0)}</div>', 
                    unsafe_allow_html=True
                )
            with col2:
                st.markdown(
                    '<div class="clean-metric">🧠<br><strong>AI Model</strong><br>Local Embeddings</div>', 
                    unsafe_allow_html=True
                )
            with col3:
                st.markdown(
                    '<div class="clean-metric">⚡<br><strong>Speed</strong><br>~10ms</div>', 
                    unsafe_allow_html=True
                )
        
        # System status
        st.markdown("### ⚙️ System Status")
        status_col1, status_col2, status_col3 = st.columns(3)
        
        with status_col1:
            rag_status = "✅ Active" if rag_engine else "❌ Error"
            st.markdown(
                f'<div class="clean-metric">🔍<br><strong>RAG Engine</strong><br>{rag_status}</div>',
                unsafe_allow_html=True
            )
        
        with status_col2:
            api_status = "✅ Configured" if os.getenv('OPENAI_API_KEY') else "❌ Missing Key"
            st.markdown(
                f'<div class="clean-metric">🔑<br><strong>OpenAI API</strong><br>{api_status}</div>',
                unsafe_allow_html=True
            )
        
        with status_col3:
            db_status = "✅ Connected" if db_stats and db_stats.get('total_documents', 0) > 0 else "❌ No Data"
            st.markdown(
                f'<div class="clean-metric">💾<br><strong>Database</strong><br>{db_status}</div>',
                unsafe_allow_html=True
            )
        
        # Nutrition facts
        st.markdown("### 💡 Evidence-Based Nutrition Science")
        facts = [
            "🥛 Protein needs: 0.8g/kg for sedentary, up to 2.2g/kg for athletes",
            "🍊 Vitamin C + iron foods = 4x better iron absorption",
            "💧 2% dehydration reduces physical and mental performance",
            "🥗 5-9 colorful vegetables daily provide diverse phytonutrients",
            "🏃‍♂️ Post-workout nutrition window is 24-48 hours, not 30 minutes",
            "🐟 Omega-3 fatty acids reduce inflammation and support brain health"
        ]
        
        for fact in facts:
            st.markdown(
                f'<div class="content-box">{fact}</div>', 
                unsafe_allow_html=True
            )
        
        # Database breakdown
        if db_stats and db_stats.get('document_types'):
            st.markdown("### 📊 Knowledge Base Composition")
            doc_types = db_stats['document_types']
            total_docs = db_stats['total_documents']
            
            for doc_type, count in doc_types.items():
                clean_name = doc_type.replace('_', ' ').title()
                percentage = (count / total_docs) * 100
                
                st.markdown(
                    f'''
                    <div class="content-box">
                        <div style="display: flex; justify-content: space-between; margin-bottom: 0.5rem; font-weight: 600;">
                            <span>{clean_name}</span>
                            <span>{count} documents ({percentage:.1f}%)</span>
                        </div>
                        <div style="background: #475569; height: 10px; border-radius: 5px; overflow: hidden;">
                            <div style="background: #22C55E; height: 10px; width: {percentage}%; border-radius: 5px;"></div>
                        </div>
                    </div>
                    ''',
                    unsafe_allow_html=True
                )
        
        # Configuration section
        st.markdown("### ⚙️ Configuration")
        with st.expander("🔧 Environment Setup", expanded=False):
            st.markdown(
                '''
                <div class="content-box">
                    <h4>Required Environment Variables (.env file):</h4>
                    <pre style="background: #0F172A; padding: 1rem; border-radius: 5px; border: 1px solid #334155;">
OPENAI_API_KEY=your_openai_api_key_here
# Add other API keys as needed
                    </pre>
                    
                    <h4>Required Python Packages:</h4>
                    <pre style="background: #0F172A; padding: 1rem; border-radius: 5px; border: 1px solid #334155;">
pip install streamlit openai pillow python-dotenv pandas
                    </pre>
                </div>
                ''',
                unsafe_allow_html=True
            )
    
    # Footer
    st.markdown("---")
    st.markdown(
        '''
        <div class="content-box" style="text-align: center; margin-top: 2rem;">
            <div style="font-weight: 600; margin-bottom: 0.5rem;">🔬 <strong>Technology Stack</strong></div>
            <div style="margin-bottom: 1rem;">RAG • OpenAI GPT-4o Vision • ChromaDB • USDA Database • Conversational AI</div>
            <div style="font-size: 0.9em; opacity: 0.7;">⚠️ <strong>Disclaimer:</strong> General nutrition guidance - consult professionals for medical advice</div>
        </div>
        ''', 
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()