"""
Quick fix for OpenAI API configuration
Run this to test and fix the OpenAI API key issue
"""

import os
from pathlib import Path
from dotenv import load_dotenv

def test_openai_config():
    print("🔧 Testing OpenAI API Configuration...")
    print("=" * 50)
    
    # Load environment variables from project root
    root_path = Path(__file__).parent.parent
    env_path = root_path / '.env'
    
    print(f"📁 Looking for .env file at: {env_path}")
    print(f"📁 File exists: {env_path.exists()}")
    
    if env_path.exists():
        load_dotenv(env_path)
        api_key = os.getenv('OPENAI_API_KEY')
        
        if api_key:
            print(f"🔑 API Key found: {api_key[:10]}...{api_key[-4:] if len(api_key) > 14 else '[short]'}")
            
            # Test the API key
            try:
                import openai
                openai.api_key = api_key
                
                # Simple test call
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",  # Use cheaper model for testing
                    messages=[{"role": "user", "content": "Say hello"}],
                    max_tokens=10
                )
                
                print("✅ OpenAI API working correctly!")
                print(f"💬 Test response: {response.choices[0].message.content}")
                return True
                
            except Exception as e:
                print(f"❌ OpenAI API error: {e}")
                
                if "401" in str(e):
                    print("🔍 This looks like an invalid API key")
                    print("💡 Please check your API key at: https://platform.openai.com/api-keys")
                elif "quota" in str(e).lower():
                    print("💳 This looks like a quota/billing issue")
                    print("💡 Please check your OpenAI billing at: https://platform.openai.com/account/billing")
                
                return False
        else:
            print("❌ No OPENAI_API_KEY found in environment")
            return False
    else:
        print("❌ .env file not found")
        return False

def create_working_env_example():
    """Create a working .env example"""
    env_content = '''# Working .env configuration
OPENAI_API_KEY=your_actual_key_here
APP_NAME=Nutrition Tutor Bot
DEBUG=False
LOG_LEVEL=INFO
OPENAI_MODEL=gpt-3.5-turbo
EMBEDDING_MODEL=text-embedding-ada-002
MAX_TOKENS=1000
TEMPERATURE=0.7'''
    
    print("\n📝 Example .env file content:")
    print("-" * 30)
    print(env_content)
    print("-" * 30)
    print("💡 Make sure to replace 'your_actual_key_here' with your real API key")

if __name__ == "__main__":
    working = test_openai_config()
    
    if not working:
        print("\n🔧 TROUBLESHOOTING STEPS:")
        print("1. Check your .env file in the project root")
        print("2. Verify your OpenAI API key is valid")
        print("3. Ensure you have billing set up on OpenAI")
        print("4. Try using gpt-3.5-turbo instead of gpt-4 (cheaper)")
        
        create_working_env_example()
    else:
        print("\n🎉 OpenAI configuration is working!")
        print("🚀 Your nutrition bot should now work fully!")