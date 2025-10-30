# db.py
import sqlite3
from contextlib import closing

DB = "data.db"

def init_db():
    with closing(sqlite3.connect(DB)) as conn:
        cur = conn.cursor()
        cur.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            first_name TEXT,
            balance REAL DEFAULT 0
        )""")
        conn.commit()

def get_user(user_id):
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("SELECT user_id, first_name, balance FROM users WHERE user_id=?", (user_id,))
        row = cur.fetchone()
        return row

def ensure_user(user_id, first_name=""):
    if not get_user(user_id):
        with sqlite3.connect(DB) as conn:
            cur = conn.cursor()
            cur.execute("INSERT INTO users (user_id, first_name, balance) VALUES (?, ?, ?)", (user_id, first_name, 0.0))
            conn.commit()

def get_balance(user_id):
    row = get_user(user_id)
    return row[2] if row else 0.0

def change_balance(user_id, amount):
    ensure_user(user_id)
    with sqlite3.connect(DB) as conn:
        cur = conn.cursor()
        cur.execute("UPDATE users SET balance = balance + ? WHERE user_id=?", (amount, user_id))
        conn.commit()
        cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
        return cur.fetchone()[0]
