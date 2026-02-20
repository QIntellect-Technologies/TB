import os
import sys
import json
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from rag_engine import RAGEngine

def test_context_flow():
    load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))
    engine = RAGEngine()
    
    # Simulate Dialogue Flow
    history = []
    
    def chat(q):
        print(f"\n❓ User: {q}")
        # Enhance query
        enhanced = engine.enhance_query_with_context(q, history)
        if enhanced != q:
            print(f"🔗 Enhanced: {enhanced}")
        
        # Generate answer
        res = engine.generate_answer(enhanced, original_query=q)
        print(f"🤖 Bot: {res['answer']}")
        
        # Update history
        history.append(f"Q: {q}")
        history.append(f"A: {res['answer']}")
        return res['answer']

    print("--- SIMULATING FLOW ---")
    chat("what are the types of tb")
    chat("which one is the most common?")
    chat("why?")
    chat("explain more detail this type") # Should stay on Pulmonary
    
    print("\n--- TEST: URDU EMPATHY ---")
    chat("مجھے ڈر لگ رہا ہے، مجھے پتا چلا ہے کہ مجھے ٹی بی ہے۔ میں کیا کروں؟") # Should NOT repeat types list

if __name__ == "__main__":
    test_context_flow()
