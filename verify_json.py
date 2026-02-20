import os
import sys
import json
from dotenv import load_dotenv

# Add backend to path
sys.path.append(os.path.join(os.getcwd(), 'backend'))

from rag_engine import RAGEngine

def test_final_json():
    load_dotenv(os.path.join(os.getcwd(), 'backend', '.env'))
    engine = RAGEngine()
    
    results = {}
    
    # 1. Test "What is TB"
    print("Testing Query 1...")
    res1 = engine.generate_answer("What is TB?")
    results["what_is_tb"] = res1["answer"]
    
    # 2. Test "Types of TB"
    print("Testing Query 2...")
    res2 = engine.generate_answer("What are the types of TB?")
    results["types_of_tb"] = res2["answer"]
    
    # 3. Test Variety
    print("Testing Query 3...")
    res3 = engine.generate_answer("How to prevent TB?")
    results["prevent_tb"] = res3["answer"]

    with open("final_report.json", "w") as f:
        json.dump(results, f, indent=4)
    print("Final report saved to final_report.json")

if __name__ == "__main__":
    test_final_json()
