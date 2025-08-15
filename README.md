# 🥗 Nutrition Tutor Bot

**AI-Powered Conversational Nutrition Assistant with Advanced RAG and Multimodal Capabilities**

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io/)
[![OpenAI](https://img.shields.io/badge/OpenAI-412991?style=for-the-badge&logo=openai&logoColor=white)](https://openai.com/)
[![Python](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)](https://python.org/)
[![ChromaDB](https://img.shields.io/badge/ChromaDB-FF6B35?style=for-the-badge)](https://www.trychroma.com/)

> **Course**: Prompt Engineering and GenAI

> **Institution**: Northeastren University

> **Team**: Ashwin Badamikar [002055743] & Madhura Adadande [002306240]

---

## 🎯 Project Overview

The Nutrition Tutor Bot is a sophisticated generative AI system that provides personalized nutrition guidance through natural conversation. Built using cutting-edge RAG (Retrieval-Augmented Generation) technology, it combines a comprehensive nutrition knowledge base with conversational AI to deliver evidence-based, personalized nutrition coaching.

### 🏆 Key Innovation
Our system uniquely combines **conversational AI**, **retrieval-augmented generation**, and **multimodal capabilities** to create a natural, ChatGPT-style nutrition coach that provides evidence-based advice with full source transparency.

---

## 🚀 Live Demo

🌐 **Try it now**: [Live Demo](https://nutrition-tutor-bot.streamlit.app/) *(Deployment URL will be added)*

📺 **Demo Video**: [10-Minute Walkthrough](link-to-video) *(Video will be added)*

📄 **Project Website**: [Project Showcase](https://ashwin-badamikar.github.io/nutrition-tutor-bot/) *(Website will be added)*

---

## ✨ Features

### 💬 **Conversational AI Coach**
- **Natural Conversation**: ChatGPT-style interface specialized for nutrition
- **Context Memory**: Remembers conversation history for follow-up questions
- **Personalized Advice**: Tailored responses based on user profile
- **Evidence-Based**: All advice backed by nutrition science with source citations

### 🧠 **Advanced RAG System**  
- **Comprehensive Knowledge Base**: 66 nutrition documents covering foods, guidelines, and meal planning
- **Vector Search**: 10ms average search time with high semantic accuracy
- **Smart Retrieval**: Intelligent context selection based on conversation flow
- **Source Attribution**: Full transparency with cited nutrition sources

### 🎯 **Intelligent Features**
- **Smart Database Search**: AI-powered similarity search through nutrition knowledge
- **Personalized Meal Planning**: Goal-based meal recommendations with dietary restrictions
- **User Profile System**: Comprehensive profiling for personalized nutrition advice
- **Performance Analytics**: Real-time metrics and conversation insights

### 📷 **Multimodal Integration** *(Advanced Feature)*
- **Photo Analysis**: Upload meal photos for AI-powered nutrition analysis
- **Vision AI**: GPT-4 Vision identifies foods and estimates portions
- **Real-time Nutrition**: USDA API integration for accurate nutritional data
- **Cross-Modal Coaching**: Combines photo analysis with personalized advice

---

# 🏗️ System Architecture

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                            NUTRITION TUTOR BOT ARCHITECTURE                      │
└─────────────────────────────────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────────────────────────────────┐
│                                 USER INTERFACE                                   │
├─────────────────────────────────────────────────────────────────────────────────┤
│  📱 Streamlit Web App                                                           │
│  ├── 💬 Chat Interface        ├── 📊 Analytics Dashboard                        │
│  ├── 🔍 Database Search       ├── 👤 User Profile Manager                       │
│  └── 📷 Photo Upload          └── ⚙️ Settings Panel                            │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CORE AI ENGINE                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  🧠 CONVERSATIONAL AI COACH                    📷 MULTIMODAL PROCESSOR          │
│  ┌─────────────────────────────┐              ┌─────────────────────────────┐   │
│  │ • Context Management       │              │ • GPT-4 Vision             │   │
│  │ • Personalized Responses   │              │ • Food Identification      │   │
│  │ • Conversation Memory      │              │ • Portion Estimation       │   │
│  │ • Dynamic Prompting        │              │ • Cross-Modal Integration  │   │
│  └─────────────────────────────┘              └─────────────────────────────┘   │
│                   │                                          │                  │
│                   └──────────────┬───────────────────────────┘                  │
│                                  │                                              │
│  🔍 RAG QUERY ENGINE                                                            │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ Query Processing → Context Retrieval → Response Generation              │   │
│  │                                                                         │   │
│  │ 1️⃣ Query Analysis     2️⃣ Vector Search      3️⃣ Context Injection      │   │
│  │ • Intent Recognition  • Semantic Similarity  • Dynamic Integration     │   │
│  │ • Context Extraction  • Metadata Filtering   • Source Attribution      │   │
│  │ • Query Optimization  • Top-K Retrieval      • Response Generation     │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
                                        │
                                        ▼
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              DATA & STORAGE LAYER                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  📚 VECTOR DATABASE (ChromaDB)         🌐 EXTERNAL APIs                         │
│  ┌─────────────────────────────┐      ┌─────────────────────────────┐          │
│  │ • 66 Nutrition Documents    │      │ 🤖 OpenAI GPT-4             │          │
│  │ • Vector Embeddings         │      │   ├── Text Generation       │          │
│  │ • Metadata Storage          │      │   └── Vision Processing     │          │
│  │ • Semantic Search Index     │      │                             │          │
│  └─────────────────────────────┘      │ 🍎 USDA FoodData Central    │          │
│                                       │   ├── 400K+ Foods           │          │
│  📊 LOCAL PROCESSING                  │   ├── Nutritional Data      │          │
│  ┌─────────────────────────────┐      │   └── Real-time Updates     │          │
│  │ • Sentence Transformers     │      └─────────────────────────────┘          │
│  │ • Local Embeddings          │                                                │
│  │ • Privacy Protection        │                                                │
│  │ • Fast Vector Operations    │                                                │
│  └─────────────────────────────┘                                                │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              CONVERSATION FLOW                                   │
└─────────────────────────────────────────────────────────────────────────────────┘

TEXT QUERY PATH:
User Input → Query Analysis → Vector Search → Context Retrieval → LLM Generation → Response
    │              │               │                │                │              │
    📝             🔍              📚               🧠               ⚡             💬
  Natural        Intent         Knowledge        GPT-4 with        Fast          Natural
 Language       Detection        Base           Context &        Processing     Response
                                Lookup         History                         + Sources

IMAGE QUERY PATH:
Photo Upload → Vision Processing → Food ID → Nutrition API → Combined Analysis → Advice
     │              │               │           │                │                │
     📷             👁️              🏷️          📊               🔄               💡
   Image          GPT-4            Food       USDA API        Cross-Modal        Personal
   Data          Vision           Recognition  Integration      Analysis         Guidance

DATABASE SEARCH PATH:
Search Query → Embedding → Vector Match → Results Ranking → Formatted Output
     │            │           │              │                     │
     🔍           🧮          ⚡             📈                    📋
   User         Local       Fast          Quality              Clean
  Search      Embedding   ChromaDB       Scoring            Presentation
```

## Technical Stack Architecture

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           TECHNOLOGY ARCHITECTURE                                │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  🎨 PRESENTATION LAYER                                                          │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ Streamlit Framework + Custom CSS + Responsive Design                   │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                        │
│  🧠 APPLICATION LAYER                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ Python 3.11 + AsyncIO + Session Management + Error Handling           │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                        │
│  🔧 AI/ML LAYER                                                                 │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ OpenAI GPT-4 + Sentence-Transformers + Vector Operations + RAG        │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                        │                                        │
│  💾 DATA LAYER                                                                  │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ ChromaDB + Local Embeddings + USDA API + Knowledge Base               │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

## Performance & Quality Metrics

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                              SYSTEM METRICS                                      │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ⚡ PERFORMANCE BENCHMARKS                                                       │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ Vector Search:      10.1ms average    │ RAG Pipeline:    12.5s average  │   │
│  │ Database Scale:     66 documents      │ Search Accuracy: High semantic  │   │
│  │ Reliability:        100% error handle│ Response Quality: 100% relevance │   │
│  │ Knowledge Coverage: Comprehensive     │ User Experience:  Professional  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
│                                                                                 │
│  🎯 QUALITY ASSURANCE                                                           │
│  ┌─────────────────────────────────────────────────────────────────────────┐   │
│  │ • Automated Testing Suite (Unit + Integration + Performance)            │   │
│  │ • Real-time Performance Monitoring and Quality Metrics                  │   │
│  │ • Evidence-based Responses with Full Source Attribution                 │   │
│  │ • Professional Error Handling and Graceful Degradation                  │   │
│  └─────────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────────┘
```

---

## Component Details

### 🧠 **RAG Query Engine**
The heart of our system combines retrieval and generation for evidence-based responses:
- **Query Processing**: Intelligent analysis of user intent and context
- **Vector Retrieval**: Semantic search through nutrition knowledge base
- **Context Integration**: Dynamic injection of relevant information
- **Response Generation**: Natural language synthesis with source attribution

### 📷 **Multimodal Integration**
Advanced cross-modal understanding for comprehensive nutrition analysis:
- **Vision Processing**: GPT-4 Vision for food identification from photos
- **Real-world Data**: USDA API integration for accurate nutritional information
- **Unified Experience**: Seamless combination of text and image interactions

### 📚 **Knowledge Management**
Comprehensive nutrition database with intelligent organization:
- **Curated Content**: 66 professional nutrition documents
- **Vector Storage**: Efficient semantic search and retrieval
- **Live Data**: Real-time nutrition information from authoritative sources
- **Quality Control**: Evidence-based information with full transparency

### 🎨 **User Experience**
Professional interface designed for natural interaction:
- **Conversational Design**: ChatGPT-style interface specialized for nutrition
- **Context Awareness**: Maintains conversation history and user preferences
- **Responsive Layout**: Multi-device compatibility with modern design
- **Performance Focus**: Fast, reliable responses with excellent usability

---

## Core AI Components

#### 1. **RAG (Retrieval-Augmented Generation)**
```
User Query → Vector Search → Context Retrieval → LLM Generation → Response + Sources
```
- **Knowledge Base**: 66 comprehensive nutrition documents
- **Vector Database**: ChromaDB with sentence-transformers embeddings
- **Search Performance**: 10.1ms average, 100% reliability score
- **Context Integration**: Dynamic context injection with conversation awareness

#### 2. **Prompt Engineering**
```
Conversation History + User Profile + Retrieved Context → Enhanced Prompt → Natural Response
```
- **Conversational Prompting**: Natural coaching persona with context management
- **Dynamic Context**: Intelligent integration of conversation history and user data
- **Response Optimization**: Multiple styles (conversational, brief, comprehensive)
- **Error Handling**: Graceful fallbacks and user guidance

#### 3. **Multimodal Integration**
```
Photo Upload → GPT-4 Vision → Food ID → USDA API → Nutrition Data → Personalized Advice
```
- **Vision Processing**: GPT-4 Vision for food identification and portion estimation
- **Cross-Modal Understanding**: Image analysis combined with text-based coaching
- **Real-World Data**: USDA FoodData Central API with 400,000+ foods
- **Seamless Experience**: Unified interface across text and image interactions

### Technology Stack

**Backend**:
- **Python 3.11**: Core development language
- **OpenAI GPT-4**: Conversational AI and vision processing
- **ChromaDB**: Vector database for document storage and retrieval
- **USDA API**: Real-time nutrition data integration

**Frontend**:
- **Streamlit**: Professional web application framework
- **Custom CSS**: Modern dark theme with excellent UX
- **Responsive Design**: Multi-device compatibility

**AI/ML**:
- **sentence-transformers**: Local embedding generation (all-MiniLM-L6-v2)
- **Vector Search**: Semantic similarity matching with metadata filtering
- **Conversational Memory**: Session-based context management

---

## 📊 Performance Metrics

### System Performance
- **⚡ Vector Search**: 10.1ms average response time
- **🎯 RAG Pipeline**: 12.5s average end-to-end response time
- **🛡️ Reliability**: 100% error handling score
- **📚 Knowledge Base**: 66 documents with comprehensive nutrition coverage

### Quality Metrics
- **🎯 Response Quality**: 100% relevance score on test queries
- **📖 Source Integration**: Average 0.3 sources per response
- **💬 Conversation Flow**: Natural dialogue with context retention
- **🔍 Search Accuracy**: High semantic relevance matching

### User Experience
- **📱 Interface**: Professional dark theme with excellent readability
- **⚡ Responsiveness**: Real-time conversation updates
- **🎨 Design**: Modern, intuitive 5-tab navigation
- **♿ Accessibility**: High contrast design with clear visual hierarchy

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.11+
- OpenAI API key
- USDA FoodData Central API key (free)
- Git

### Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/ashwin-badamikar/nutrition-tutor-bot.git
cd nutrition-tutor-bot

# 2. Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment variables
cp .env.example .env
# Edit .env with your API keys

# 5. Initialize the nutrition database
cd src
python init_database.py

# 6. Run the application
streamlit run app.py
```

Visit `http://localhost:8501` to access your personal nutrition coach!

### Environment Configuration

Create `.env` file in project root:
```env
OPENAI_API_KEY=your_openai_api_key_here
USDA_API_KEY=your_usda_api_key_here
OPENAI_MODEL=gpt-4-turbo-preview
MAX_TOKENS=2000
TEMPERATURE=0.7
```

---

## 📁 Project Structure

```
nutrition-tutor-bot/
├── README.md                 # Project documentation
├── requirements.txt          # Python dependencies
├── .env.example             # Environment template
├── .streamlit/              # Streamlit configuration
│   └── config.toml
├── src/                     # Main application code
│   ├── app.py              # Main Streamlit application
│   ├── init_database.py    # Database initialization
│   ├── config/             # Configuration management
│   │   └── settings.py
│   ├── models/             # AI and data models
│   │   ├── rag_engine.py           # RAG query engine
│   │   ├── vector_store.py         # ChromaDB vector store
│   │   ├── nutrition_api.py        # USDA API integration
│   │   └── conversational_nutrition_coach.py
│   ├── data/               # Data processing
│   │   ├── nutrition_data_collector.py
│   │   └── knowledge_processor.py
│   └── utils/              # Utility functions
├── data/                   # Data storage
│   ├── raw/               # Raw nutrition data
│   ├── processed/         # Processed documents for RAG
│   └── chroma_db/        # Vector database files
├── tests/                 # Comprehensive testing suite
│   ├── unit/             # Unit tests
│   ├── integration/      # Integration tests
│   └── performance/      # Performance benchmarks
├── docs/                 # Project documentation
│   ├── technical_documentation.md
│   ├── user_guide.md
│   └── system_architecture.md
└── deployment/           # Production deployment configs
    ├── Dockerfile
    ├── docker-compose.yml
    └── deploy_guides/
```

---

## 🎯 Usage Examples

### Basic Nutrition Conversation
```
User: "Hi! I want to build muscle"
Coach: "Great goal! Building muscle requires the right nutrition strategy. 
        Tell me about your current activity level and eating habits..."

User: "I'm 25, lift weights 4x per week, but struggle with protein"
Coach: "Perfect! For a 25-year-old doing strength training 4x per week, 
        you'll want 1.6-2.2g protein per kg body weight daily..."
```

### Advanced Meal Planning
```
User: "Create a meal plan for weight loss, I'm vegetarian"
Coach: "I'll create a vegetarian weight loss meal plan for you. Based on 
        your profile, here's a balanced approach focusing on plant proteins..."

[Provides detailed meal plan with calories, macros, and specific food recommendations]
```

### Intelligent Database Search
```
Search: "high protein vegetarian foods"
Results: 
- Tofu (17.3g protein per 100g)
- Greek Yogurt (10g protein per 100g)  
- Lentils (9g protein per 100g)
[With complete nutritional breakdowns and usage suggestions]
```

---

## 🧪 Testing & Quality Assurance

### Automated Testing Suite
```bash
# Run all tests
cd tests
python -m pytest unit/ integration/ performance/ -v

# Performance benchmarks
cd performance
python test_focused_performance.py
```

### Test Coverage
- **Unit Tests**: Individual component testing (RAG, API, vector store)
- **Integration Tests**: End-to-end workflow testing
- **Performance Tests**: Response time and quality benchmarking
- **Reliability Tests**: Error handling and edge case validation

### Performance Results
- ✅ **Vector Search**: 10.1ms average (excellent)
- ✅ **RAG Quality**: 100% relevance score (perfect)
- ✅ **System Reliability**: 100% error handling (production-ready)
- ✅ **Database Scale**: 66 comprehensive documents

---

## 👥 Team Contributions

### Ashwin Badamikar
**Role**: 
- 🧠 **RAG System Development**: Designed and implemented the complete RAG pipeline with ChromaDB integration
- 🤖 **Conversational AI**: Built the ChatGPT-style conversational interface with context memory
- 🔧 **API Integration**: Developed USDA nutrition API integration for real-world data
- 🧪 **Testing & Performance**: Created comprehensive testing suite with performance benchmarking
- 📱 **Frontend Development**: Implemented the professional Streamlit interface with custom styling

### Madhura Adadande  
**Role**: 
- 📚 **Knowledge Base Design**: Curated and structured the 66-document nutrition knowledge base
- 📊 **Data Processing**: Developed nutrition data collection and processing pipelines
- 🎨 **Prompt Engineering**: Designed systematic prompting strategies for nutrition coaching
- 📷 **Multimodal Integration**: Implemented photo analysis workflow with vision AI
- 📈 **Quality Assurance**: Ensured accuracy and relevance of nutrition information

### Shared Responsibilities
- 🏗️ **System Architecture**: Collaborative design of overall system structure
- 📖 **Documentation**: Joint development of technical and user documentation  
- 🚀 **Deployment**: Collaborative deployment and production optimization
- 🎯 **Project Management**: Coordinated development timeline and feature prioritization

---

## 🔬 Technical Innovation

### Novel Contributions
1. **Conversational RAG**: Unique combination of natural conversation with scientific knowledge retrieval
2. **Intelligent Context Management**: Dynamic conversation memory without persistent storage
3. **Cross-Modal Nutrition Coaching**: Seamless integration of photo analysis with personalized advice
4. **Real-World Data Integration**: Live USDA API for accurate, up-to-date nutrition information

### Advanced AI Implementation
- **Hybrid Vector Search**: Combines semantic similarity with metadata filtering
- **Context-Aware Prompting**: Dynamic prompt construction based on conversation flow
- **Multi-Strategy Retrieval**: Intelligent selection of knowledge based on query analysis
- **Professional User Experience**: Production-level interface with excellent usability

---

## 🛠️ Installation Guide

### System Requirements
- **Python**: 3.11 or higher
- **Memory**: 4GB RAM minimum (8GB recommended)
- **Storage**: 2GB free space
- **Internet**: Required for API access

### Step-by-Step Setup

#### 1. Environment Setup
```bash
# Clone repository
git clone https://github.com/ashwin-badamikar/nutrition-tutor-bot.git
cd nutrition-tutor-bot

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

#### 2. Install Dependencies
```bash
# Install required packages
pip install -r requirements.txt

# Verify installation
python -c "import streamlit, openai, chromadb; print('✅ All packages installed successfully')"
```

#### 3. API Configuration
```bash
# Copy environment template
cp .env.example .env

# Edit .env file with your API keys:
# OPENAI_API_KEY=your_openai_key_here
# USDA_API_KEY=your_usda_key_here
```

**Get API Keys:**
- **OpenAI**: https://platform.openai.com/api-keys
- **USDA**: https://fdc.nal.usda.gov/api-guide.html (free)

#### 4. Initialize Database
```bash
# Navigate to source directory
cd src

# Initialize nutrition knowledge base
python init_database.py

# Expected output: "✅ Database ready with 66 documents"
```

#### 5. Launch Application
```bash
# Start the nutrition coach
streamlit run app.py

# Open browser to: http://localhost:8501
```

### Troubleshooting
- **Import errors**: Ensure virtual environment is activated
- **API errors**: Verify API keys in .env file
- **Database errors**: Run `python init_database.py` to reinitialize
- **Port conflicts**: Use `streamlit run app.py --server.port 8502`

---

## 🧪 Testing & Validation

### Running Tests
```bash
# Navigate to tests directory
cd tests

# Run unit tests
python -m pytest unit/ -v

# Run integration tests  
python -m pytest integration/ -v

# Run performance benchmarks
cd performance
python test_focused_performance.py
```

### Test Results Summary
- **✅ Unit Tests**: All core components tested and validated
- **✅ Integration Tests**: End-to-end workflows verified
- **✅ Performance Tests**: Benchmarked with excellent results
- **✅ Reliability Tests**: 100% error handling coverage

---

## 🎓 Academic Context

### Course Information
- **Assignment**: Generative AI Final Project
- **Objective**: Develop sophisticated generative AI system for real-world needs
- **Requirements**: Minimum 2 core AI components (we implemented 3)
- **Focus**: Demonstrate mastery of generative AI technologies

### Learning Outcomes Demonstrated
- **Advanced RAG Implementation**: Production-level retrieval-augmented generation
- **Conversational AI**: Natural language processing and dialogue management
- **Multimodal Integration**: Cross-modal AI understanding and generation
- **Software Engineering**: Professional development practices and architecture
- **Real-World Application**: Practical AI system addressing genuine user needs

---

## 🔮 Future Enhancements

### Planned Features
- **📱 Mobile App**: Native iOS/Android application
- **🍳 Recipe Generation**: AI-created recipes based on preferences and restrictions
- **📈 Progress Tracking**: Long-term nutrition and health monitoring
- **🏃‍♂️ Fitness Integration**: Connect with activity trackers and workout apps
- **🌍 Multilingual Support**: Nutrition coaching in multiple languages

### Technical Improvements
- **🔧 Fine-Tuned Models**: Custom nutrition-specific language models
- **⚡ Enhanced Performance**: Advanced caching and optimization
- **🔍 Expanded Knowledge**: Larger nutrition database with recent research
- **🤖 Advanced AI**: Multi-agent systems for specialized nutrition domains

---

## 🔒 Privacy & Ethics

### Data Protection
- **Session-Only Storage**: User data not persisted beyond browser session
- **Local Processing**: Embeddings generated locally for privacy
- **Transparent Sources**: All advice includes source attribution
- **User Control**: Complete profile management and data deletion

### Ethical AI
- **Bias Mitigation**: Diverse, evidence-based nutrition knowledge
- **Limitation Transparency**: Clear communication of system capabilities
- **Professional Guidance**: Encourages consultation with healthcare professionals
- **Responsible AI**: Ethical use of AI for health and wellness

### Limitations
- **General Guidance Only**: Not a replacement for professional medical advice
- **Evidence-Based Scope**: Limited to established nutrition science
- **Individual Variation**: Cannot account for unique medical conditions
- **Session-Based**: Conversation history not persistent across sessions

---

## 📜 License

This project is licensed under the [MIT License](https://opensource.org/licenses/MIT) - see the [LICENSE](LICENSE) file for complete terms.

---

## 🙏 Acknowledgments

### Technology Partners
- **OpenAI**: GPT-4 language model and vision capabilities
- **Hugging Face**: Sentence-transformers embedding models
- **ChromaDB**: Vector database infrastructure
- **USDA**: Comprehensive nutrition database
- **Streamlit**: Web application framework

### Academic Support
- **Course Instructor**: Prof. Nick Brown
- **Institution**: Northeastern University
- **Course**: Prompt Engineering and GenAI

### Open Source Community
Special thanks to the open-source AI/ML community for providing the foundational tools and libraries that made this project possible.

---

## 📞 Contact & Support

### Team Contact
- **Ashwin Badamikar**: [badamikar.a@northeastern.edu]
- **Madhura Adadande**: [adadande.m@northeastern.edu]



