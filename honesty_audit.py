import json
import os

def analyze_dataset(path, name):
    print(f"📊 Analyzing {name} at {path}...")
    if not os.path.exists(path):
        print(f"❌ File not found: {path}")
        return None
        
    try:
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        qa = data.get('qa_pairs', [])
        total = len(qa)
        
        if total == 0:
            return None

        ans_lengths = [len(x['answer']) for x in qa]
        avg_len = sum(ans_lengths) / total if total > 0 else 0
        detailed = len([x for x in ans_lengths if x > 500])
        concise = len([x for x in ans_lengths if x < 200])
        
        words = set()
        for x in qa:
            words.update(x['question'].split())
        
        return {
            "Total": total,
            "Avg Answer Length": f"{avg_len:.1f} chars",
            "Detailed (>500)": f"{detailed} ({detailed/total*100:.1f}%)",
            "Concise (<200)": f"{concise} ({concise/total*100:.1f}%)",
            "Unique Question Tokens": len(words)
        }
    except Exception as e:
        print(f"❌ Error analyzing {name}: {e}")
        return None

def honest_review():
    eng_path = 'dataset/TB_QA_DATASET_ENGLISH.json'
    urdu_path = 'dataset/TB_QA_DATASET_URDU_100K.json'
    
    eng_stats = analyze_dataset(eng_path, "English V5.1")
    urdu_stats = analyze_dataset(urdu_path, "Urdu 60K")
    
    if not eng_stats or not urdu_stats:
        print("❌ Could not complete comparison due to missing data.")
        return

    print("\n" + "="*70)
    print("🏆 THE HONEST VERDICT: SIDE-BY-SIDE")
    print("="*70)
    
    metrics = ["Total", "Avg Answer Length", "Detailed (>500)", "Concise (<200)", "Unique Question Tokens"]
    
    header = f"{'Metric':<25} | {'English (V5.1)':<20} | {'Urdu (60K)':<20}"
    print(header)
    print("-" * len(header))
    
    for m in metrics:
        print(f"{m:<25} | {str(eng_stats[m]):<20} | {str(urdu_stats[m]):<20}")

if __name__ == "__main__":
    honest_review()
