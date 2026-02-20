import json

# Load the dataset
with open('dataset/TB_QA_DATASET_50K_ULTIMATE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*80)
print("TB Q&A DATASET ANALYSIS")
print("="*80)

# Metadata
print("\n📊 METADATA:")
for key, value in data['metadata'].items():
    print(f"  {key}: {value}")

# Category breakdown
categories = {}
for qa in data['qa_pairs']:
    cat = qa['category']
    categories[cat] = categories.get(cat, 0) + 1

print("\n📂 CATEGORIES:")
total_q = len(data['qa_pairs'])
print(f"{'Category':<40} | {'Count':<10} | {'Percentage':<10}")
print("-" * 70)
for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    print(f"{cat:<40} | {count:<10,} | {count/total_q*100:.1f}%")
print("-" * 70)
print(f"{'TOTAL':<40} | {total_q:<10,} | 100.0%")

# Sample questions from different categories
print("\n📝 SAMPLE QUESTIONS:")
seen_categories = set()
for qa in data['qa_pairs']:
    if qa['category'] not in seen_categories:
        print(f"\n  Category: {qa['category']}")
        print(f"  Q: {qa['question']}")
        print(f"  A: {qa['answer'][:100]}...")
        seen_categories.add(qa['category'])
        if len(seen_categories) >= 5:
            break

# Show some variety
print("\n🎯 QUESTION VARIETY EXAMPLES:")
print("\n  Drug-related questions:")
for i in [0, 12, 25, 37]:
    if i < len(data['qa_pairs']):
        print(f"    - {data['qa_pairs'][i]['question']}")

print("\n  Treatment-related questions:")
treatment_qs = [qa for qa in data['qa_pairs'] if 'Treatment' in qa['category']]
for i in range(min(5, len(treatment_qs))):
    print(f"    - {treatment_qs[i]['question']}")

print("\n" + "="*80)
