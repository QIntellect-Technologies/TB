import sqlite3
import json

def debug_urdu():
    db_path = 'backend/tb_expert.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print("Checking some Urdu records...")
    cursor.execute("SELECT question FROM qa_index WHERE language='Urdu' LIMIT 5")
    rows = cursor.fetchall()
    for r in rows:
        print(f"Record: {r[0]}")
        
    print("\nTesting manual LIKE search for 'کھانسی'...")
    # FTS5 might need different handling for some characters, checking LIKE as fallback
    cursor.execute("SELECT question FROM qa_index WHERE question LIKE '%کھانسی%' LIMIT 1")
    row = cursor.fetchone()
    if row:
        print(f"✅ Found via LIKE: {row[0]}")
    else:
        print("❌ Not found via LIKE either.")
        
    conn.close()

if __name__ == "__main__":
    debug_urdu()
