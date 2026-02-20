#!/usr/bin/env python3
"""
Analyze existing TB dataset for conversational question coverage
Identifies gaps in yes/no, comparison, and practical questions
"""

import json
import re
from collections import defaultdict

def analyze_dataset(file_path):
    """Analyze dataset for conversational question patterns"""
    
    print(f"📂 Loading dataset from {file_path}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    qa_pairs = data.get('qa_pairs', [])
    total = len(qa_pairs)
    print(f"✅ Loaded {total:,} Q&A pairs\n")
    
    # Conversational patterns to check
    patterns = {
        'yes_no_is': r'^Is\s+',
        'yes_no_can': r'^Can\s+',
        'yes_no_does': r'^Does\s+',
        'yes_no_do': r'^Do\s+',
        'yes_no_are': r'^Are\s+',
        'yes_no_will': r'^Will\s+',
        'comparison': r'(difference between|vs|versus|compared to)',
        'how_long': r'^How long',
        'what_happens': r'^What happens if',
        'why': r'^Why\s+',
        'what_is_simple': r'^What is\s+\w+\s*\?$',  # Simple "What is X?" questions
    }
    
    # Track matches
    matches = defaultdict(list)
    
    for qa in qa_pairs:
        question = qa.get('question', '')
        
        for pattern_name, pattern in patterns.items():
            if re.search(pattern, question, re.IGNORECASE):
                matches[pattern_name].append(question)
    
    # Print analysis
    print("=" * 80)
    print("CONVERSATIONAL QUESTION ANALYSIS")
    print("=" * 80)
    
    for pattern_name, questions in sorted(matches.items()):
        count = len(questions)
        percentage = (count / total) * 100
        print(f"\n{pattern_name.upper().replace('_', ' ')}:")
        print(f"  Count: {count:,} ({percentage:.2f}%)")
        print(f"  Examples:")
        for q in questions[:5]:
            print(f"    - {q}")
    
    # Calculate gaps
    print("\n" + "=" * 80)
    print("IDENTIFIED GAPS")
    print("=" * 80)
    
    # Critical conversational questions that should exist
    critical_questions = [
        "Is TB contagious?",
        "Can TB be cured?",
        "Is TB viral or bacterial?",
        "Can children get TB?",
        "Is TB serious?",
        "Can TB spread through food?",
        "Is TB preventable?",
        "Can TB come back after treatment?",
        "Is TB worse than COVID?",
        "What's the difference between latent and active TB?",
        "How long does TB treatment last?",
        "How long to stay home with TB?",
        "What happens if I stop TB medicine early?",
        "What happens if TB is left untreated?",
        "Why is TB treatment so long?",
        "Why do I need 4 drugs for TB?",
        "Can I go to work with TB?",
        "Can I drink alcohol during TB treatment?",
    ]
    
    all_questions_lower = [q.get('question', '').lower() for q in qa_pairs]
    
    missing = []
    found = []
    
    for cq in critical_questions:
        if cq.lower() in all_questions_lower:
            found.append(cq)
        else:
            missing.append(cq)
    
    print(f"\n✅ FOUND ({len(found)}/{len(critical_questions)}):")
    for q in found:
        print(f"  - {q}")
    
    print(f"\n❌ MISSING ({len(missing)}/{len(critical_questions)}):")
    for q in missing:
        print(f"  - {q}")
    
    # Summary
    print("\n" + "=" * 80)
    print("SUMMARY")
    print("=" * 80)
    print(f"Total Q&A pairs: {total:,}")
    print(f"Conversational questions found: {sum(len(v) for v in matches.values()):,}")
    print(f"Critical questions missing: {len(missing)}/{len(critical_questions)}")
    print(f"\n💡 Recommendation: Generate ~{len(missing) * 100:,} conversational Q&A pairs")
    
    return {
        'total': total,
        'matches': matches,
        'missing_critical': missing,
        'found_critical': found
    }

if __name__ == "__main__":
    # Analyze English dataset
    result = analyze_dataset("dataset/TB_QA_DATASET_50K_ULTIMATE_V5.json")
    
    print("\n✅ Analysis complete!")
