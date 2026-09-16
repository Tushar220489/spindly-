import sqlite3
from datetime import date

from werkzeug.security import check_password_hash, generate_password_hash

DB_PATH = "expense_tracker.db"


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL REFERENCES users(id),
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            created_at TEXT DEFAULT (datetime('now'))
        )
    """)
    conn.commit()
    conn.close()


def seed_db():
    conn = get_db()

    if conn.execute("SELECT COUNT(*) FROM users").fetchone()[0] > 0:
        conn.close()
        return

    password_hash = generate_password_hash("demo123")
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        ("Demo User", "demo@spendly.com", password_hash),
    )
    user_id = cursor.lastrowid

    ym = date.today().strftime("%Y-%m")
    sample_expenses = [
        (user_id, 45.50, "Food",          f"{ym}-02", "Groceries at Trader Joe's"),
        (user_id, 12.00, "Transport",     f"{ym}-03", "Metro card top-up"),
        (user_id, 89.99, "Bills",         f"{ym}-05", "Electricity bill"),
        (user_id, 25.00, "Health",        f"{ym}-08", "Pharmacy pickup"),
        (user_id, 15.75, "Entertainment", f"{ym}-10", "Movie tickets"),
        (user_id, 60.00, "Shopping",      f"{ym}-14", "New running shoes"),
        (user_id,  8.25, "Food",          f"{ym}-18", "Coffee and lunch"),
        (user_id, 20.00, "Other",         f"{ym}-21", "Miscellaneous purchase"),
    ]
    conn.executemany(
        "INSERT INTO expenses (user_id, amount, category, date, description) "
        "VALUES (?, ?, ?, ?, ?)",
        sample_expenses,
    )
    conn.commit()
    conn.close()


def get_user_by_email(email):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()
    return user


def create_user(name, email, password):
    conn = get_db()
    password_hash = generate_password_hash(password)
    cursor = conn.execute(
        "INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)",
        (name, email, password_hash),
    )
    conn.commit()
    user_id = cursor.lastrowid
    conn.close()
    return user_id


def authenticate_user(email, password):
    conn = get_db()
    user = conn.execute(
        "SELECT * FROM users WHERE email = ?", (email,)
    ).fetchone()
    conn.close()

    if user and check_password_hash(user["password_hash"], password):
        return user
    return None
