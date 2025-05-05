import os
import sqlite3

APP_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DB_PATH = os.path.join(APP_DIR, "database", "notifications.db")

os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

def init_db():
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS notifications (
                user_id INTEGER PRIMARY KEY
            )
        """)
        db.commit()

def subscribe_user(user_id):
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("INSERT OR IGNORE INTO notifications (user_id) VALUES (?)", (user_id,))
        db.commit()

def unsubscribe_user(user_id):
    with sqlite3.connect(DB_PATH) as db:
        cursor = db.cursor()
        cursor.execute("DELETE FROM notifications WHERE user_id = ?", (user_id,))
        db.commit()

def is_subscribed(user_id):
    try:
        with sqlite3.connect(DB_PATH) as db:
            cursor = db.cursor()
            cursor.execute("SELECT 1 FROM notifications WHERE user_id = ?", (user_id,))
            return cursor.fetchone() is not None
    except sqlite3.OperationalError as e:
        print(f"Erro ao acessar o banco de dados: {e}")
        return False
def get_all_users():
    try:
        with sqlite3.connect(DB_PATH) as db:
            cursor = db.cursor()
            cursor.execute("SELECT user_id FROM notifications")
            return [row[0] for row in cursor.fetchall()]
    except sqlite3.OperationalError as e:
        print(f"[DB] Erro ao buscar usuários: {e}")
        return []
