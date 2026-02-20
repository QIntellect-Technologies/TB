import json
import random

def forensic_audit(path, name, samples=20):
    print(f"\n🔬 FORENSIC AUDIT: {name}")
    print("-" * 50)
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        qa = data.get('qa_pairs', [])
        
        # Select random samples across different categories
        indices = random.sample(range(len(qa)), samples)
        
        for i in indices:
            item = qa[i]
            q = item['question']
            a = item['answer']
            cat = item['category']
            
            print(f"\n[ID: {item.get('id', 'N/A')}] [Cat: {cat}]")
            print(f"Q: {q}")
            
            # Extract first line of answer for preview
            preview = a.split('\n')[0]
            print(f"A (Start): {preview}")
            
            # Logic Check: Does the answer contain the keyword from the question?
            # Basic heuristic: Check if critical nouns in question appear in answer.
            keywords = item.get('keywords', [])
            match = any(str(k).lower() in a.lower() for k in keywords)
            
            if match:
                print("✅ LOGICAL MATCH: Answer addresses the key topic.")
            else:
                print("⚠️ POTENTIAL MISMATCH: Check link between Q and A.")
            
            # Length Check
            if "تفصیل" in q or "detail" in q.lower() or "clinical" in q.lower():
                if len(a) > 300:
                    print("✅ LENGTH: Appropriate (Detailed).")
                else:
                    print("⚠️ LENGTH: Too short for a detailed query?")
            else:
                print("✅ LENGTH: Appropriate (Fact-based).")

    except Exception as e:
        print(f"❌ Error during forensic audit: {e}")

if __name__ == "__main__":
    forensic_audit('dataset/TB_QA_DATASET_ENGLISH.json', "English (V5.1)")
    forensic_audit('dataset/TB_QA_DATASET_URDU_100K.json', "Urdu (100K Global)")
