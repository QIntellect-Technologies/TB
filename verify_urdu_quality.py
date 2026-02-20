import json
import re

def check_urdu_quality():
    print("🔍 AUDITING URDU DATASET...")
    try:
        with open('dataset/TB_QA_DATASET_URDU_100K.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ Error loading file: {e}")
        return

    qa_pairs = data.get('qa_pairs', [])
    total = len(qa_pairs)
    print(f"📉 Total Questions: {total}")

    errors = {
        "english_question_mark": 0,
        "missing_question_mark": 0,
        "english_period_in_answer": 0,
        "mixed_script_question": 0  # Latin chars in Question
    }

    samples = []

    for i, item in enumerate(qa_pairs):
        q = item['question']
        a = item['answer']
        
        # Check 1: Ends with English ? instead of Urdu ؟
        if q.strip().endswith("?"):
            errors["english_question_mark"] += 1
            if len(samples) < 3: samples.append(f"Eng ?: {q}")

        # Check 2: No Question Mark at all
        if not (q.strip().endswith("?") or q.strip().endswith("؟")):
            errors["missing_question_mark"] += 1
            if len(samples) < 5: samples.append(f"Missing ?: {q}")

        # Check 3: Mixed Script (Checking for a-z in question, ignoring IDs if any)
        # We expect Questions to be pure Urdu mostly.
        if re.search(r'[a-zA-Z]', q):
            # Allow things in parentheses maybe? But user asked for Pure Urdu.
            # Let's count them to see extent.
            errors["mixed_script_question"] += 1
            if len(samples) < 8: samples.append(f"Mixed: {q}")

    print("\n📊 ERROR STATS:")
    for k, v in errors.items():
        print(f"  - {k}: {v} ({v/total*100:.1f}%)")

    print("\n📝 SAMPLES:")
    for s in samples:
        print(f"  {s}")

if __name__ == "__main__":
    check_urdu_quality()
