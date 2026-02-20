import sqlite3

def debug_search(query):
    db_path = 'backend/tb_expert.db'
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    print(f"DEBUG: Searching for '{query}'")
    # Clean query for FTS5 (remove special chars)
    clean_q = "".join(c for c in query if c.isalnum() or c.isspace())
    
    try:
        cursor.execute("SELECT question, answer FROM qa_index WHERE qa_index MATCH ? LIMIT 3", (clean_q,))
        rows = cursor.fetchall()
        if rows:
            for r in rows:
                print(f"FOUND: {r[0]}")
        else:
            print("❌ NO MATCH FOUND via FTS5 MATCH")
            
            # Try LIKE as backup to see if data exists
            cursor.execute("SELECT question FROM qa_index WHERE question LIKE ? LIMIT 3", (f"%{clean_q}%",))
            rows = cursor.fetchall()
            if rows:
                print(f"⚠️ FOUND via LIKE (Index exists but MATCH failed): {rows[0][0]}")
            else:
                print("❌ DATA NOT FOUND in database at all.")
    except Exception as e:
        print(f"ERROR: {e}")
    conn.close()

if __name__ == "__main__":
    debug_search("What is tb")
    debug_search("TB")
    debug_search("Bedaquiline")
