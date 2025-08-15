import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    def __init__(self):
        # API Configuration
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        self.usda_api_key = os.getenv("USDA_API_KEY", "")  # ADD THIS LINE
        self.pinecone_api_key = os.getenv("PINECONE_API_KEY", "")
        self.pinecone_environment = os.getenv("PINECONE_ENVIRONMENT", "")
        
        # App Configuration
        self.app_name = os.getenv("APP_NAME", "Nutrition Tutor Bot")
        self.debug = os.getenv("DEBUG", "False").lower() == "true"
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        
        # Model Configuration
        self.openai_model = os.getenv("OPENAI_MODEL", "gpt-4-turbo-preview")
        self.embedding_model = os.getenv("EMBEDDING_MODEL", "text-embedding-ada-002")
        self.max_tokens = int(os.getenv("MAX_TOKENS", "2000"))
        self.temperature = float(os.getenv("TEMPERATURE", "0.7"))
        
        # RAG Configuration
        self.chunk_size = 1000
        self.chunk_overlap = 200
        self.top_k_results = 5

settings = Settings()