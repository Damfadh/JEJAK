import sqlite3
import json
import pprint

DB = "backend/pki.db"

def main():
    conn = sqlite3.connect(DB)
    c = conn.cursor()
    rows = c.execute("SELECT id,timestamp,publisher_id,doc_id,recipient_id,result,raw_payload FROM audit ORDER BY id DESC LIMIT 10").fetchall()
    pprint.pprint(rows)
    conn.close()

if __name__ == '__main__':
    main()
