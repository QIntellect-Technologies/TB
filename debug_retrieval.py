#!/usr/bin/env python3
"""
Debug Retrieval Quality
Analyzes why specific questions are fetching wrong contexts
"""
import sys
import os
from dotenv import load_dotenv

sys.path.append('backend')
load_dotenv('backend/.env')

from rag_engine import RAGEngine

def debug_retrieval(questions):
    with open('retrieval_log_xray.txt', 'w', encoding='utf-8') as f:
        f.write("=" * 80 + "\n")
        f.write("🚑 X-RAY DIAGNOSTIC\n")
        f.write("=" * 80 + "\n")
        
        rag = RAGEngine()
        
        for q in questions:
            f.write(f"\n🔍 QUESTION: '{q}'\n")
            f.write("-" * 80 + "\n")
            
            # Use top_k=10 as per new config
            results = rag.retrieve_context(q, top_k=10)
            
            f.write(f"   Found {len(results)} docs\n")
            
            has_xray = False
            for i, doc in enumerate(results, 1):
                category = doc.get('category', 'Unknown')
                relevance = doc.get('relevance_score', 0)
                answer = doc.get('answer', '')
                preview = answer[:200].replace('\n', ' ')
                
                f.write(f"   {i}. [{category}] (Score: {relevance:.4f})\n")
                f.write(f"      Context: {preview}...\n")
                
                if "x-ray" in answer.lower():
                    f.write("      ✅ FOUND X-RAY IN THIS DOC\n")
                    has_xray = True
            
            if not has_xray:
                 f.write("\n❌ NO X-RAY MENTION FOUND IN TOP 10\n")

if __name__ == "__main__":
    debug_questions = [
        "Can TB be detected with an X-ray?",
        "Chest X-ray for TB diagnosis"
    ]
    debug_retrieval(debug_questions)
