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

def save_message(chat_id: int, sender: str, message: str):
    conn = sqlite3.connect("chat_memory.db")
    c = conn.cursor()
    c.execute('INSERT INTO messages (chat_id, sender, message) VALUES (?, ?, ?)',
              (chat_id, sender, message))
    conn.commit()
    conn.close()

def get_recent_messages(chat_id: int, limit: int = 5):
    conn = sqlite3.connect("chat_memory.db")
    c = conn.cursor()
    c.execute('SELECT sender, message FROM messages WHERE chat_id = ? ORDER BY timestamp DESC LIMIT ?',
              (chat_id, limit))
    rows = c.fetchall()
    conn.close()
    # restituisce i messaggi in ordine cronologico
    return rows[::-1]