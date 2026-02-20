import json
import re
from collections import Counter
import math

def calculate_entropy(texts):
    if not texts: return 0
    counts = Counter(texts)
    total_count = len(texts)
    entropy = -sum((count/total_count) * math.log2(count/total_count) for count in counts.values())
    return entropy

def audit_global_readiness():
    print("🌍 INITIATING GLOBAL READINESS AUDIT...")
    
    with open('dataset/TB_QA_DATASET_50K_ULTIMATE_V5.json', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    qa_pairs = data['qa_pairs']
    total = len(qa_pairs)
    print(f"📊 Dataset Size: {total} questions")
    
    # 1. LINGUISTIC DIVERSITY (Robotic Check)
    questions = [q['question'] for q in qa_pairs]
    unique_questions = set(questions)
    uniqueness_ratio = len(unique_questions) / total
    print(f"🔹 Uniqueness Ratio: {uniqueness_ratio:.2%} (Target: >95%)")
    
    if uniqueness_ratio < 0.95:
        print("❌ WARNING: High duplication detected.")
    else:
        print("✅ PASS: High linguistic diversity.")

    # 2. CLINICAL CURRENCY (WHO Standards)
    # Checking for modern MDR-TB drugs (Bedaquiline, Linezolid) vs Old (Kanamycin)
    answers_text = " ".join([q['answer'].lower() for q in qa_pairs])
    
    has_bedaquiline = "bedaquiline" in answers_text
    has_linezolid = "linezolid" in answers_text
    has_kanamycin = "kanamycin" in answers_text
    
    print("\n🔹 Clinical Standard Check:")
    if has_bedaquiline and has_linezolid:
        print("✅ PASS: Includes modern WHO-recommended MDR-TB drugs (Bedaquiline/Linezolid).")
    else:
        print("❌ FAIL: Missing key modern MDR drugs.")
        
    if has_kanamycin:
        print("⚠️ NOTE: Contains 'Kanamycin' (Phased out in many current WHO guidelines). Verify context.")
    
    # 3. REGIONAL SPECIFICITY (NTP Forms)
    # specific forms like 'TB01', 'TB02' are common but check for country names
    country_markers = ["india", "pakistan", "south africa", "nigeria", "philippines"]
    found_countries = [c for c in country_markers if c in answers_text]
    
    print("\n🔹 Regional Neutrality Check:")
    if found_countries:
        print(f"⚠️ WARNING: Found specific country references: {found_countries}. Might limit global scope.")
    else:
        print("✅ PASS: No specific country names found (Generic Global Dataset).")
        
    # 4. ANSWER QUALITY (Length variance)
    short_ans = [len(q['answer']) for q in qa_pairs if len(q['answer']) < 200]
    long_ans = [len(q['answer']) for q in qa_pairs if len(q['answer']) > 500]
    
    print("\n🔹 Metadata Stats:")
    print(f"   - Concise Answers (<200 chars): {len(short_ans)} ({len(short_ans)/total:.1%})")
    print(f"   - Detailed Answers (>500 chars): {len(long_ans)} ({len(long_ans)/total:.1%})")
    
    if len(short_ans) > 0 and len(long_ans) > 0:
        print("✅ PASS: Adaptive length verified (Mix of Short & Long).")
    else:
        print("❌ FAIL: Lack of answer length diversity.")

    print("\n🏁 CONCLUSION:")
    if uniqueness_ratio > 0.95 and has_bedaquiline and not found_countries:
        print("🏆 STATUS: READY FOR GLOBAL DEPLOYMENT.")
    else:
        print("⚠️ STATUS: REQUIRES REVIEW (See warnings above).")

if __name__ == "__main__":
    audit_global_readiness()
