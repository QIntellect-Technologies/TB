import json
import sqlite3
import os
import time

def index_datasets():
    print("🚀 INITIALIZING HIGH-PERFORMANCE INDEXER...")
    db_path = 'backend/tb_expert.db'
    
    # Cleanup previous DB if exists
    if os.path.exists(db_path):
        os.remove(db_path)
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    # Create Virtual Table for Full-Text Search (FTS5)
    # Using porter tokenizer for English, and unicode61 for multilingual support
    cursor.execute("""
        CREATE VIRTUAL TABLE qa_index USING fts5(
            id,
            language,
            category,
            question,
            answer,
            keywords,
            tokenize = "unicode61"
        )
    """)
    
    datasets = [
        ('English', 'dataset/TB_QA_DATASET_ENGLISH.json'),
        ('Urdu', 'dataset/TB_QA_DATASET_URDU_100K.json')
    ]
    
    total_indexed = 0
    start_time = time.time()
    
    for lang, path in datasets:
        print(f"📂 Processing {lang} dataset: {path}...")
        if not os.path.exists(path):
            print(f"⚠️ Skip: {path} not found.")
            continue
            
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            qa_pairs = data.get('qa_pairs', [])
            
            # Batch insertion for speed
            batch = []
            for item in qa_pairs:
                batch.append((
                    item.get('id', ''),
                    lang,
                    item.get('category', ''),
                    item.get('question', ''),
                    item.get('answer', ''),
                    ",".join(item.get('keywords', []))
                ))
                
                if len(batch) >= 1000:
                    cursor.executemany("INSERT INTO qa_index (id, language, category, question, answer, keywords) VALUES (?, ?, ?, ?, ?, ?)", batch)
                    total_indexed += len(batch)
                    batch = []
            
            # Insert remaining
            if batch:
                cursor.executemany("INSERT INTO qa_index (id, language, category, question, answer, keywords) VALUES (?, ?, ?, ?, ?, ?)", batch)
                total_indexed += len(batch)

    conn.commit()
    conn.close()
    
    duration = time.time() - start_time
    print(f"\n✅ INDEXING COMPLETE!")
    print(f"📊 Total Records: {total_indexed:,}")
    print(f"⏱️ Time Taken: {duration:.2f} seconds")
    print(f"💾 Database Size: {os.path.getsize(db_path) / (1024*1024):.2f} MB")

if __name__ == "__main__":
    index_datasets()
