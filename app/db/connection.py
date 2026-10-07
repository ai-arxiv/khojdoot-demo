import sqlite3
from pathlib import Path

db_path = Path(__file__).resolve().parents[2] / "khoj_doot.db"

def get_connection():
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA foreign_keys = ON")
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_connection()
    schema_path = Path(__file__).resolve().parents[2] / "schema.sql"

    with open(schema_path, "r") as file:
        conn.executescript(file.read())

    conn.commit()
    conn.close()