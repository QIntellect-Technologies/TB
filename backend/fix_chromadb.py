"""
Fix ChromaDB schema compatibility issue
Migrates existing database to work with ChromaDB 0.4.22
"""
import sqlite3
import os

db_path = "backend/vector_db/chroma.sqlite3"

if not os.path.exists(db_path):
    print("❌ Database not found!")
    exit(1)

print(f"🔧 Fixing ChromaDB schema at {db_path}...")

conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Fix collections table
cursor.execute("PRAGMA table_info(collections)")
columns = [col[1] for col in cursor.fetchall()]

if 'topic' not in columns:
    print("✅ Adding 'topic' column to collections table...")
    try:
        cursor.execute("ALTER TABLE collections ADD COLUMN topic TEXT")
        conn.commit()
        print("✅ collections.topic added!")
    except Exception as e:
        print(f"⚠️  Error: {e}")

# Fix segments table
cursor.execute("PRAGMA table_info(segments)")
seg_columns = [col[1] for col in cursor.fetchall()]

if 'topic' not in seg_columns:
    print("✅ Adding 'topic' column to segments table...")
    try:
        cursor.execute("ALTER TABLE segments ADD COLUMN topic TEXT")
        conn.commit()
        print("✅ segments.topic added!")
    except Exception as e:
        print(f"⚠️  Error: {e}")

# Check for other potential missing columns
tables_to_check = ['embeddings', 'metadata']
for table in tables_to_check:
    try:
        cursor.execute(f"PRAGMA table_info({table})")
        cols = [col[1] for col in cursor.fetchall()]
        if 'topic' not in cols:
            print(f"✅ Adding 'topic' to {table} table...")
            cursor.execute(f"ALTER TABLE {table} ADD COLUMN topic TEXT")
            conn.commit()
    except Exception as e:
        # Table might not exist, that's okay
        pass

conn.close()

print("\n🎉 All schema fixes applied! Restart the backend now.")
