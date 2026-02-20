import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from rag_engine import RAGEngine

def test_failover():
    # Force load from backend/.env
    env_path = os.path.join(os.getcwd(), 'backend', '.env')
    print(f"📂 Loading env from: {env_path}")
    load_dotenv(env_path)
    
    print("🚀 Initializing Multi-API RAG Engine...")
    engine = RAGEngine()
    
    test_queries = [
        "Is TB contagious?",        # Medical (Factual)
        "do you know who i am",     # Identity (Small Talk)
        "what can you do for me",   # Capability (Small Talk)
        "what is tb",               # Medical (Factual)
        "I am scared. help me",     # Medical (Emotional)
        "how are you today?"        # Small Talk
    ]
    
    for query in test_queries:
        print(f"\n❓ Query: {query}")
        result = engine.generate_answer(query)
        print(f"✅ Answer: {result['answer'][:100]}...")
        print(f"📊 Method: {result.get('method')}")

if __name__ == "__main__":
    test_failover()
