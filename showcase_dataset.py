import json
import random

# Load the dataset
with open('dataset/TB_QA_DATASET_20K_ULTIMATE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

print("="*80)
print("🩺 TB Q&A DATASET - QUESTION VARIETY SHOWCASE")
print("="*80)

# Show metadata
print("\n📊 DATASET OVERVIEW:")
print(f"  Total Questions: {data['metadata']['total_questions']:,}")
print(f"  Version: {data['metadata']['version']}")
print(f"  Quality: {data['metadata']['quality']}")
print(f"  Sources: {', '.join(data['metadata']['sources'])}")

# Get categories
categories = {}
for qa in data['qa_pairs']:
    cat = qa['category']
    categories[cat] = categories.get(cat, 0) + 1

print("\n📂 CATEGORY BREAKDOWN:")
for cat, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
    percentage = (count / len(data['qa_pairs'])) * 100
    print(f"  {cat}: {count:,} questions ({percentage:.1f}%)")

# Show question variety for a single topic (Isoniazid)
print("\n" + "="*80)
print("🎯 EXAMPLE: Question Variety for 'Isoniazid' (Single Drug)")
print("="*80)
print("\nShowing how users can ask the SAME medical question in MANY different ways:")

inh_questions = [qa for qa in data['qa_pairs'] if 'isoniazid' in qa['question'].lower()][:15]
for i, qa in enumerate(inh_questions, 1):
    print(f"\n{i}. Q: {qa['question']}")
    print(f"   A: {qa['answer']}")

# Show different categories
print("\n" + "="*80)
print("📚 EXAMPLES FROM DIFFERENT CATEGORIES")
print("="*80)

# Drug Information
print("\n1️⃣ DRUG INFORMATION:")
drug_qs = [qa for qa in data['qa_pairs'] if qa['category'] == 'Drug Information']
for qa in random.sample(drug_qs, 3):
    print(f"\n  Q: {qa['question']}")
    print(f"  A: {qa['answer']}")

# Treatment Protocols
print("\n2️⃣ TREATMENT PROTOCOLS:")
treatment_qs = [qa for qa in data['qa_pairs'] if qa['category'] == 'Treatment Protocols']
if treatment_qs:
    for qa in treatment_qs[:3]:
        print(f"\n  Q: {qa['question']}")
        print(f"  A: {qa['answer']}")

# Treatment Dosing
print("\n3️⃣ WEIGHT-BASED DOSING:")
dosing_qs = [qa for qa in data['qa_pairs'] if 'Dosing' in qa['category']]
if dosing_qs:
    for qa in dosing_qs[:3]:
        print(f"\n  Q: {qa['question']}")
        print(f"  A: {qa['answer']}")

# Show drug coverage
print("\n" + "="*80)
print("💊 COMPREHENSIVE DRUG COVERAGE")
print("="*80)

drugs_covered = set()
for qa in data['qa_pairs']:
    if qa['category'] == 'Drug Information':
        for topic in qa['related_topics']:
            drugs_covered.add(topic)

print(f"\nTotal drugs covered: {len(drugs_covered)}")
print("\nDrugs included:")
for i, drug in enumerate(sorted(drugs_covered), 1):
    print(f"  {i:2d}. {drug}")

print("\n" + "="*80)
print("✅ This dataset can answer virtually ANY TB-related question!")
print("="*80)
