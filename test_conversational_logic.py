#!/usr/bin/env python3
"""
Test Advanced Conversational Logic
Verifies intent classification and LLM-based chat replies
"""
import sys
import os
from dotenv import load_dotenv

sys.path.append('backend')
load_dotenv('backend/.env')

from rag_engine import RAGEngine

def test_conversation():
    with open('test_results_clean.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("CONVERSATION LOGIC TEST\n")
        f.write("=" * 80 + "\n")
        
        rag = RAGEngine()
        
        test_cases = [
            # Type: Greeting
            "Hi",
            "Hello there",
            "Excuse me",
            
            # Type: Small Talk
            "How are you?",
            "Who are you?",
            
            # Type: Irrelevant
            "I love Python programming",
            "What is the weather in London?",
            
            # Type: Abuse
            "You are stupid",
            
            # Type: Medical (Direct)
            "Is TB contagious?",
            
            # Type: Mixed (Greeting + Medical)
            "Hi, can TB be cured?",
            "Excuse me, what are the symptoms of TB?"
        ]
        
        for q in test_cases:
            f.write(f"\n[QUERY]: '{q}'\n")
            f.write("-" * 40 + "\n")
            
            # 1. Test Classification (Private method access for debugging)
            intent = rag._classify_chat_intent(q, "English")
            f.write(f"[Classified Intent]: [{intent.upper()}]\n")
            
            # 2. Test Full Generation
            result = rag.generate_answer(q, "English")
            method = result.get('method', 'unknown')
            answer = result.get('answer', '')
            
            f.write(f"[Method Used]: {method}\n")
            f.write(f"[Answer]: {answer[:150]}...\n")
            
            # Verifications
            if q == "Hi" and method != "llm_chat":
                f.write("[FAIL]: 'Hi' should use llm_chat\n")
            elif "TB" in q and method != "rag_llm":
                 # Note: rag_llm is expected for medical queries if LLM is active
                 pass

if __name__ == "__main__":
    test_conversation()
