import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "wildex.db"


def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    return conn

def init_db():
    with get_conn() as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS wild (
                region      TEXT NOT NULL,
                id          INTEGER NOT NULL,
                name        TEXT NOT NULL,
                type        TEXT,
                description TEXT,
                PRIMARY KEY (region, id)
            )
        """)

def get_regions():
    with get_conn() as conn:
        rows = conn.execute("SELECT DISTINCT region FROM wild ORDER BY region")
        return [r["region"] for r in rows]


def get_grouped():
    with get_conn() as conn:
        rows = conn.execute("SELECT * FROM wild ORDER BY region, id")
        grouped = {}

        for r in rows:
            grouped.setdefault(r["region"],[]).append(dict(r))
        
        return grouped


def wild_by_id(region, wid):
    with get_conn() as conn:
        row = conn.execute(
            "SELECT * FROM wild WHERE region = ? AND id = ?", (region, wid)
        ).fetchone()
        return dict(row) if row else None