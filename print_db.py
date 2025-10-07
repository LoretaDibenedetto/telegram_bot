import sqlite3

def create_db():
    conn = sqlite3.connect("chat_memory.db")
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS messages (
            chat_id INTEGER,
            sender TEXT,
            message TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def print_db_content():
    create_db()
    try:
        conn = sqlite3.connect("chat_memory.db")
        c = conn.cursor()
        c.execute('SELECT chat_id, sender, message, timestamp FROM messages ORDER BY timestamp DESC')
        rows = c.fetchall()
        print(f"Numero di record trovati: {len(rows)}")

        for row in rows:
            print(f"Chat {row[0]} | {row[1]}: {row[2]} | {row[3]}")
    except Exception as e:
        print(f"Errore durante la lettura del database: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    print_db_content()
