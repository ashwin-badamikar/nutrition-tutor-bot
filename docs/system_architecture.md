# System Architecture - Nutrition Tutor Bot

## High-Level Architecture Diagram

```mermaid
graph TB
    subgraph "User Interface Layer"
        UI[Streamlit Web App]
        Chat[Chat Interface]
        Search[Database Search]
        Meal[Meal Planning]
        Photo[Photo Analysis]
    end
    
    subgraph "Application Layer"
        RAG[RAG Engine]
        Coach[Conversational Coach]
        Profile[Profile Manager]
        API[API Manager]
    end
    
    subgraph "Data Layer"
        VDB[(Vector Database<br/>ChromaDB)]
        KB[Knowledge Base<br/>66 Documents]
        Session[Session State<br/>User Data]
    end
    
    subgraph "External APIs"
        OpenAI[OpenAI GPT-4<br/>+ Vision]
        USDA[USDA Nutrition<br/>Database]
    end
    
    subgraph "AI/ML Components"
        Embeddings[Local Embeddings<br/>sentence-transformers]
        Search_Engine[Vector Search<br/>Similarity Matching]
    end
    
    %% User Interface Connections
    UI --> Chat
    UI --> Search
    UI --> Meal
    UI --> Photo
    
    %% Application Layer Connections
    Chat --> Coach
    Chat --> RAG
    Search --> RAG
    Meal --> RAG
    Photo --> API
    
    %% Data Flow
    Coach --> RAG
    RAG --> VDB
    RAG --> KB
    Profile --> Session
    
    %% External API Connections
    Coach --> OpenAI
    RAG --> OpenAI
    API --> USDA
    Photo --> OpenAI
    
    %% AI/ML Connections
    KB --> Embeddings
    Embeddings --> VDB
    VDB --> Search_Engine
    Search_Engine --> RAG
    
    %% Styling
    classDef uiLayer fill:#E3F2FD
    classDef appLayer fill:#E8F5E8
    classDef dataLayer fill:#FFF3E0
    classDef apiLayer fill:#F3E5F5
    classDef aiLayer fill:#E0F2F1
    
    class UI,Chat,Search,Meal,Photo uiLayer
    class RAG,Coach,Profile,API appLayer
    class VDB,KB,Session dataLayer
    class OpenAI,USDA apiLayer
    class Embeddings,Search_Engine aiLayer
```

## RAG Pipeline Architecture

```mermaid
sequenceDiagram
    participant User
    participant UI as Streamlit UI
    participant Coach as Conversational Coach
    participant RAG as RAG Engine
    participant VDB as Vector Database
    participant LLM as OpenAI GPT-4
    participant USDA as USDA API
    
    User->>UI: Types message
    UI->>Coach: Process user input
    Coach->>Coach: Analyze conversation context
    Coach->>RAG: Enhanced query with context
    RAG->>VDB: Search for relevant documents
    VDB-->>RAG: Return similar documents
    RAG->>RAG: Rank and filter results
    RAG->>LLM: Generate response with context
    LLM-->>RAG: Natural language response
    RAG-->>Coach: Response + sources
    Coach-->>UI: Formatted response
    UI-->>User: Display conversation
    
    Note over User,USDA: For photo analysis, USDA API provides nutrition data
    Note over Coach,LLM: Conversation history maintains context
```

## Data Flow Architecture

```mermaid
flowchart LR
    subgraph "Input Sources"
        UserChat[User Chat Input]
        UserPhoto[Photo Upload]
        UserProfile[User Profile]
        UserSearch[Search Query]
    end
    
    subgraph "Processing Pipeline"
        QueryAnalysis[Query Analysis]
        ContextRetrieval[Context Retrieval]
        VectorSearch[Vector Similarity Search]
        VisionAI[GPT-4 Vision Analysis]
    end
    
    subgraph "Knowledge Sources"
        LocalKB[Local Knowledge Base<br/>66 Documents]
        USDAData[USDA Nutrition Database<br/>400k+ Foods]
        ConversationMemory[Conversation History]
    end
    
    subgraph "AI Generation"
        PromptEngineering[Prompt Engineering]
        LLMGeneration[GPT-4 Response Generation]
        ResponseFormatting[Response Formatting]
    end
    
    subgraph "Output"
        ChatResponse[Chat Response]
        SourceCitation[Source Citations]
        PersonalizedAdvice[Personalized Advice]
        NutritionData[Nutrition Data]
    end
    
    %% Input Flow
    UserChat --> QueryAnalysis
    UserPhoto --> VisionAI
    UserProfile --> PromptEngineering
    UserSearch --> VectorSearch
    
    %% Processing Flow
    QueryAnalysis --> ContextRetrieval
    ContextRetrieval --> VectorSearch
    VisionAI --> USDAData
    
    %% Knowledge Integration
    VectorSearch --> LocalKB
    VectorSearch --> ConversationMemory
    USDAData --> NutritionData
    
    %% Generation Flow
    LocalKB --> PromptEngineering
    ConversationMemory --> PromptEngineering
    PromptEngineering --> LLMGeneration
    LLMGeneration --> ResponseFormatting
    
    %% Output Flow
    ResponseFormatting --> ChatResponse
    ResponseFormatting --> SourceCitation
    ResponseFormatting --> PersonalizedAdvice
```

## Component Interaction Diagram

```mermaid
graph LR
    subgraph "Frontend Components"
        ChatUI[Chat Interface]
        SearchUI[Search Interface]
        MealUI[Meal Planning Interface]
        PhotoUI[Photo Analysis Interface]
        ProfileUI[Profile Management]
    end
    
    subgraph "Backend Services"
        RAGService[RAG Engine Service]
        VectorService[Vector Store Service]
        APIService[External API Service]
        ProfileService[Profile Service]
    end
    
    subgraph "Data Storage"
        ChromaDB[(ChromaDB<br/>Vector Storage)]
        SessionState[(Session State<br/>User Data)]
        KnowledgeBase[(Knowledge Base<br/>JSON Documents)]
    end
    
    subgraph "External Services"
        OpenAIAPI[OpenAI API<br/>GPT-4 + Vision]
        USDAAPI[USDA FoodData<br/>Central API]
    end
    
    %% Frontend to Backend
    ChatUI --> RAGService
    SearchUI --> VectorService
    MealUI --> RAGService
    PhotoUI --> APIService
    ProfileUI --> ProfileService
    
    %% Backend to Data
    RAGService --> ChromaDB
    RAGService --> KnowledgeBase
    VectorService --> ChromaDB
    ProfileService --> SessionState
    
    %% Backend to External
    RAGService --> OpenAIAPI
    APIService --> OpenAIAPI
    APIService --> USDAAPI
    
    %% Data Relationships
    KnowledgeBase --> ChromaDB
    SessionState --> RAGService
```

## Technology Stack Overview

### Core Technologies
- **Python 3.11**: Backend development
- **Streamlit**: Web application framework
- **OpenAI GPT-4**: Language model and vision AI
- **ChromaDB**: Vector database for document storage
- **Sentence Transformers**: Local embedding generation

### AI/ML Libraries
- **LangChain**: RAG pipeline components
- **sentence-transformers**: Text embedding generation
- **NumPy**: Numerical computations
- **Pandas**: Data manipulation

### Integration APIs
- **OpenAI API**: Chat completions and vision analysis
- **USDA FoodData Central**: Real-time nutrition data
- **RESTful Architecture**: Standard API communication

### Development Tools
- **pytest**: Automated testing framework
- **python-dotenv**: Environment variable management
- **Pillow**: Image processing for photo uploads
- **JSON**: Data serialization and storage

## Performance Characteristics

### Response Times
- **Vector Search**: ~10ms average
- **RAG Pipeline**: ~12.5 seconds average
- **Photo Analysis**: ~5-8 seconds
- **Database Queries**: <100ms

### Scalability Considerations
- **Local Embeddings**: No API costs for search
- **Session-based Storage**: Minimal server requirements
- **Stateless Architecture**: Easy horizontal scaling
- **Modular Design**: Components can be upgraded independently

### Resource Requirements
- **Memory**: ~500MB for embedding model + database
- **Storage**: ~100MB for knowledge base and embeddings
- **Network**: API calls only for LLM generation and nutrition lookup
- **CPU**: Moderate for local embedding generation

## Security Architecture

### Data Protection
- **Environment Variables**: Secure API key storage
- **Session Isolation**: User data isolated per session
- **No Persistence**: Sensitive data not permanently stored
- **Local Processing**: Embeddings generated locally

### API Security
- **Key Management**: Environment-based configuration
- **Rate Limiting**: Handled by external service providers
- **Error Handling**: Graceful fallbacks for API failures
- **Input Validation**: User input sanitization

### Privacy by Design
- **Minimal Data Collection**: Only necessary information stored
- **Transparent Processing**: User aware of data usage
- **User Control**: Profile editing and deletion capabilities
- **Session Cleanup**: Automatic data clearing on session end