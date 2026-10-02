import sqlite3

DB_NAME = "khoj_doot.db"


def get_db():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS shops (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            city TEXT NOT NULL,
            slug TEXT UNIQUE NOT NULL,
            updated_at TEXT NOT NULL
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS photos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id INTEGER NOT NULL,
            filename TEXT NOT NULL,
            FOREIGN KEY (shop_id) REFERENCES shops(id)
        )
    """)

    conn.execute("""
        CREATE TABLE IF NOT EXISTS bins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            shop_id INTEGER UNIQUE NOT NULL,
            data TEXT NOT NULL,
            FOREIGN KEY (shop_id) REFERENCES shops(id)
        )
    """)

    conn.commit()
    conn.close()