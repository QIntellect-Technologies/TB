#!/usr/bin/env python3
"""
Test Groq LLM Integration
Tests conversational Q&A with the new LLM-powered RAG
"""

import sys
sys.path.append('backend')

from rag_engine import RAGEngine
import os

# Load environment variables
from dotenv import load_dotenv
load_dotenv('backend/.env')

def test_conversational_qa():
    """Test conversational questions with LLM"""
    
    print("=" * 80)
    print("TESTING GROQ LLM INTEGRATION")
    print("=" * 80)
    
    # Check if API key is set
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key or groq_key == "your_groq_api_key_here":
        print("\n❌ ERROR: GROQ_API_KEY not set in backend/.env")
        print("\n📝 To fix:")
        print("1. Go to https://console.groq.com")
        print("2. Sign up (free)")
        print("3. Create API key")
        print("4. Add to backend/.env:")
        print("   GROQ_API_KEY=your_actual_key_here")
        return
    
    print(f"\n✅ Groq API key found: {groq_key[:20]}...")
    
    # Initialize RAG engine
    print("\n🔄 Initializing RAG engine...")
    rag = RAGEngine()
    
    # Test questions
    test_questions = [
        "Is TB contagious?",
        "Can TB be cured?",
        "Is TB viral or bacterial?",
        "Can children get TB?",
        "What's the difference between latent and active TB?",
        "How long does TB treatment last?",
        "What happens if I stop TB medicine early?",
        "Can I drink alcohol during TB treatment?",
    ]
    
    print("\n" + "=" * 80)
    print("TESTING CONVERSATIONAL QUESTIONS")
    print("=" * 80)
    
    for i, question in enumerate(test_questions, 1):
        print(f"\n[{i}/{len(test_questions)}] Question: {question}")
        print("-" * 80)
        
        try:
            result = rag.generate_answer(question, language="English")
            answer = result.get('answer', 'No answer')
            
            print(f"✅ Answer: {answer}")
            
            # Check if it's a good answer
            if len(answer) < 20:
                print("⚠️  Answer seems too short")
            elif "No relevant information" in answer:
                print("⚠️  No information found")
            else:
                print("✅ Good answer!")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    print("\n" + "=" * 80)
    print("TEST COMPLETE")
    print("=" * 80)

if __name__ == "__main__":
    test_conversational_qa()
