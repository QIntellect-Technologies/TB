import os
import sys
import json
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from rag_engine import RAGEngine

def test_curable_fix():
    load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))
    engine = RAGEngine()
    
    # Simulate conversation context for "it" resolution
    history = ["Q: I want to know about tb"]
    
    print("Testing Query: 'is it cureable?' with history...")
    q = "is it cureable?"
    enhanced = engine.enhance_query_with_context(q, history)
    res = engine.generate_answer(enhanced, original_query=q)
    
    print(f"RES: {res['answer']}")
    
    with open("curable_fix_report.json", "w") as f:
        json.dump({"query": q, "enhanced": enhanced, "answer": res["answer"]}, f, indent=4)

if __name__ == "__main__":
    test_curable_fix()
