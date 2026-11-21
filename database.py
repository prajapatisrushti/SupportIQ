
import sqlite3

DB_NAME = "supportiq.db"


def get_connection():
    return sqlite3.connect(DB_NAME)


def initialize_database():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS customers (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tickets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_id INTEGER,
            subject TEXT NOT NULL,
            description TEXT NOT NULL,
            category TEXT DEFAULT 'General',
            priority TEXT DEFAULT 'Medium',
            status TEXT DEFAULT 'Open',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (customer_id) REFERENCES customers(id)
        )
    """)

    # Add resolution notes column to existing databases
    cursor.execute("PRAGMA table_info(tickets)")
    columns = [column[1] for column in cursor.fetchall()]

    if "resolution_notes" not in columns:
        cursor.execute("""
            ALTER TABLE tickets
            ADD COLUMN resolution_notes TEXT DEFAULT ''
        """)

    conn.commit()
    conn.close()


def add_customer(name, email):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "INSERT OR IGNORE INTO customers (name, email) VALUES (?, ?)",
        (name, email)
    )

    conn.commit()
    conn.close()


def add_ticket(customer_id, subject, description, category, priority):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO tickets
        (customer_id, subject, description, category, priority)
        VALUES (?, ?, ?, ?, ?)
    """, (customer_id, subject, description, category, priority))

    conn.commit()
    conn.close()
