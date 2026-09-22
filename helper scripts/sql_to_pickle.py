import sqlite3
import sys
import pickle


def sql_to_pickle(db_file, pickle_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM pronunciations
    """)
    conn.commit()

    PRONUNCIATIONS = cursor.fetchall()
    
    conn.close()
    KV_PRONUNCIATIONS = {}
    
    for word, sound in PRONUNCIATIONS:
        KV_PRONUNCIATIONS[word] = sound

    print(KV_PRONUNCIATIONS['oonk'])
    with open(pickle_file, mode='wb+') as f:
        pickle.dump(KV_PRONUNCIATIONS, f)


def test_pickle_file(pickle_file):
    with open(pickle_file, mode='rb') as f:
        KV_PRONUNCIATIONS = pickle.load(f) 

    print(KV_PRONUNCIATIONS['oonk'])

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python sql_to_pickle.py <sql_file> [output_pickle_path]")
        sys.exit(1)
    
    db_path = sys.argv[1]
    pickle_path = sys.argv[2] if len(sys.argv) > 2 else "pronunciation.pkl"
    test_pickle_file(pickle_path)
    #sql_to_pickle(db_path, pickle_path)