"""
Expand TB_QA_DATASET_MASSIVE.json to 20,000+ Q&A pairs by generating variations and extracting more facts.
"""
import json
import random
import re
from tqdm import tqdm

# Load existing Q&A
with open('TB_QA_DATASET_MASSIVE.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

qa_pairs = data['qa_pairs']
existing_questions = set(q['question'].strip().lower() for q in qa_pairs)

# Helper: Generate question variations
QUESTION_TEMPLATES = [
    "Explain: {q}",
    "Can you tell me: {q}",
    "In detail, what is: {q}",
    "Summarize: {q}",
    "What should I know about {q}?",
    "How would you answer: {q}?",
    "What are the key facts about {q}?",
    "List important points about {q}.",
    "What is the clinical significance of {q}?",
    "What is the importance of {q}?",
    "What are the risks of {q}?",
    "What are the benefits of {q}?",
    "What are the causes of {q}?",
    "What are the symptoms of {q}?",
    "What are the complications of {q}?",
    "What is the management of {q}?",
    "What is the prevention of {q}?",
    "What is the treatment for {q}?",
    "What is the protocol for {q}?",
    "What is the guideline for {q}?",
    "What is the definition of {q}?"
]

# Helper: Extract all unique facts/lines from the knowledge base
with open('TB_KNOWLEDGE_BASE_GOLDEN.txt', 'r', encoding='utf-8') as f:
    kb_lines = [line.strip() for line in f if line.strip() and not line.startswith('=') and not line.startswith('#')]

fact_lines = [l for l in kb_lines if len(l) > 20 and not l.lower().startswith('table of contents')]

# Generate new Q&A pairs
new_qa = []
qid = len(qa_pairs) + 1

for fact in tqdm(fact_lines, desc="Expanding Q&A dataset"):
    # Use the fact as an answer, generate multiple question variations
    for template in random.sample(QUESTION_TEMPLATES, k=min(5, len(QUESTION_TEMPLATES))):
        # Try to extract a main topic from the fact
        topic = fact.split(':')[0] if ':' in fact else fact.split('.')[0]
        q = template.format(q=topic.strip())
        if q.lower() not in existing_questions:
            qa = {
                "id": f"Q{qid:05d}",
                "category": "Auto-Expanded",
                "question": q,
                "answer": fact,
                "keywords": re.findall(r'\b\w+\b', topic.lower()),
                "related_topics": []
            }
            new_qa.append(qa)
            existing_questions.add(q.lower())
            qid += 1
        if len(qa_pairs) + len(new_qa) >= 20000:
            break
    if len(qa_pairs) + len(new_qa) >= 20000:
        break

# Combine and save
all_qa = qa_pairs + new_qa
print(f"Total Q&A after expansion: {len(all_qa)}")
data['qa_pairs'] = all_qa
# Update metadata
data['metadata']['total_questions'] = len(all_qa)
with open('TB_QA_DATASET_MASSIVE.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
print("✅ MASSIVE Q&A dataset complete!")
