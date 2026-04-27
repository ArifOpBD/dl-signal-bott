import sqlite3

conn = sqlite3.connect("users.db", check_same_thread=False)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS users (
    chat_id INTEGER PRIMARY KEY
)
""")

conn.commit()

def add_user(chat_id):
    cur.execute("INSERT OR IGNORE INTO users VALUES (?)", (chat_id,))
    conn.commit()

def get_users():
    cur.execute("SELECT chat_id FROM users")
    return [i[0] for i in cur.fetchall()]