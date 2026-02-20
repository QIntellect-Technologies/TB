import os
import sys
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from rag_engine import RAGEngine

def test_final():
    load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))
    engine = RAGEngine()
    
    # 1. Test "What is TB" - Should include all types and be concise
    print("\n--- TEST: WHAT IS TB ---")
    res1 = engine.generate_answer("What is TB?")
    print(f"RES: {res1['answer']}")
    
    # 2. Test "Types of TB" - Should include Latent/MDR
    print("\n--- TEST: TYPES OF TB ---")
    res2 = engine.generate_answer("What are the types of TB?")
    print(f"RES: {res2['answer']}")
    
    # 3. Repeat to check for variety
    print("\n--- TEST: REPEAT FOR VARIETY ---")
    res3 = engine.generate_answer("How to prevent TB?")
    print(f"RES: {res3['answer']}")

if __name__ == "__main__":
    test_final()
