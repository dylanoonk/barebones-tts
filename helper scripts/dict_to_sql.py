import sqlite3
import sys

def dict_to_sql(dict_file, db_file="pronunciation.db"):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pronunciations (
            word TEXT PRIMARY KEY,
            sound TEXT
        )
    """)
    
    with open(dict_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
                
            parts = line.split()
            word = parts[0]
            sound = " ".join(parts[1:])
            
            cursor.execute(
                "INSERT OR REPLACE INTO pronunciations VALUES (?, ?)",
                (word, sound)
            )
    
    conn.commit()
    conn.close()
    print(f"Created {db_file}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python dict_to_sql.py <dict_file> [output_db]")
        sys.exit(1)
    
    dict_path = sys.argv[1]
    db_path = sys.argv[2] if len(sys.argv) > 2 else "pronunciation.db"
    dict_to_sql(dict_path, db_path)