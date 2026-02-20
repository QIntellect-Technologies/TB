import os
import sys
import json
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from rag_engine import RAGEngine

def test_brevity():
    load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))
    engine = RAGEngine()
    
    results = {}
    
    # 1. Default Concise Test
    print("Testing Default Concise Response...")
    res1 = engine.generate_answer("What is TB?")
    results["default_concise"] = res1["answer"]
    
    # 2. Detailed Request Test
    print("Testing Detailed Request Response...")
    res2 = engine.generate_answer("Tell me more about the types of TB")
    results["detailed_request"] = res2["answer"]
    
    # 3. Urdu Concise Test
    print("Testing Urdu Concise Response...")
    res3 = engine.generate_answer("ٹی بی کیا ہے؟")
    results["urdu_concise"] = res3["answer"]

    with open("brevity_report.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Brevity report saved to brevity_report.json")

if __name__ == "__main__":
    test_brevity()
