"""
Rebuild SQLite Database for TB Expert Search
Populates the FTS5 'qa_index' table from the master JSON datasets.
"""
import sqlite3
import json
import os
import sys

# Paths
# Paths (Absolute based on script location)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, 'backend', 'tb_expert.db')
DATASET_DIR = os.path.join(BASE_DIR, "dataset")

FILES = [
    ("English", os.path.join(DATASET_DIR, "TB_QA_DATASET_ENGLISH.json")),
    ("Urdu", os.path.join(DATASET_DIR, "TB_QA_DATASET_URDU_100K.json"))
]

def rebuild_db():
    print(f"🔧 Rebuilding SQLite database at {DB_PATH}...")
    
    # Remove existing DB to start fresh
    if os.path.exists(DB_PATH):
        try:
            os.remove(DB_PATH)
            print("🗑️  Removed existing database.")
        except Exception as e:
            print(f"⚠️  Could not remove existing DB: {e}")

    # Create DB and Table
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Enable FTS5
    # Create Virtual Table for fast full-text search
    cursor.execute("""
        CREATE VIRTUAL TABLE IF NOT EXISTS qa_index USING fts5(
            id, 
            language, 
            category, 
            question, 
            answer, 
            tokenize='porter'
        )
    """)
    
    total_added = 0
    
    for lang, file_path in FILES:
        if not os.path.exists(file_path):
            print(f"⚠️  File not found: {file_path}")
            continue
            
        print(f"📂 Processing {lang} from {file_path}...")
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            questions = []
            if isinstance(data, dict):
                questions = data.get("qa_pairs", [])
            elif isinstance(data, list):
                questions = data
                
            print(f"   Found {len(questions)} records.")
            
            # Batch insert
            batch = []
            for q in questions:
                batch.append((
                    q.get('id', 'UNK'),
                    lang,
                    q.get('category', 'General'),
                    q.get('question', ''),
                    q.get('answer', '')
                ))
                
                if len(batch) >= 1000:
                    cursor.executemany("INSERT INTO qa_index (id, language, category, question, answer) VALUES (?, ?, ?, ?, ?)", batch)
                    total_added += len(batch)
                    batch = []
                    
            if batch:
                cursor.executemany("INSERT INTO qa_index (id, language, category, question, answer) VALUES (?, ?, ?, ?, ?)", batch)
                total_added += len(batch)
                
        except Exception as e:
            print(f"❌ Error processing {file_path}: {e}")
            
    # Commit and Close
    conn.commit()
    conn.close()
    
    print(f"\n✅ Database rebuild complete!")
    print(f"📊 Total records indexed: {total_added}")

if __name__ == "__main__":
    rebuild_db()
