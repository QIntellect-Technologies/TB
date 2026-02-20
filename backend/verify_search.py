import sqlite3
import time

def verify_search():
    db_path = 'backend/tb_expert.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    
    test_queries = [
        ("Bedaquiline", "English"),
        ("رفیمپیسین", "Urdu"),
        ("cough", "English"),
        ("کھانسی", "Urdu")
    ]
    
    print(f"{'Query':<15} | {'Lang':<8} | {'Latency':<10} | {'Found?'}")
    print("-" * 50)
    
    for q, lang in test_queries:
        start = time.time()
        cursor.execute("SELECT question, language FROM qa_index WHERE qa_index MATCH ? LIMIT 1", (q,))
        row = cursor.fetchone()
        latency = (time.time() - start) * 1000
        
        found = "✅ Yes" if row else "❌ No"
        print(f"{q:<15} | {lang:<8} | {latency:>6.2f}ms | {found}")
        
    conn.close()

if __name__ == "__main__":
    verify_search()
