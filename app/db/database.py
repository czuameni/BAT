import sqlite3
from pathlib import Path

DB_PATH = Path("data/app.db")


class Database:
    def __init__(self):
        self._create_tables()

    def _connect(self):
        return sqlite3.connect(DB_PATH)

    def _create_tables(self):
        with self._connect() as conn:
            conn.execute("""
            CREATE TABLE IF NOT EXISTS versions (
                id INTEGER PRIMARY KEY,
                original_path TEXT,
                backup_path TEXT,
                hash TEXT,
                timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
            )
            """)

    # =========================
    # 💾 SAVE VERSION
    # =========================
    def save_version(self, original, backup, file_hash):
        with self._connect() as conn:
            conn.execute("""
            INSERT INTO versions (original_path, backup_path, hash)
            VALUES (?, ?, ?)
            """, (str(original), str(backup), file_hash))

    # =========================
    # 🔍 GET LAST FILE VERSION
    # =========================
    def get_file(self, path):
        with self._connect() as conn:
            cursor = conn.execute("""
            SELECT * FROM versions
            WHERE original_path = ?
            ORDER BY timestamp DESC
            LIMIT 1
            """, (str(path),))

            row = cursor.fetchone()

        if not row:
            return None

        return {
            "hash": row[3],
            "backup_path": row[2]
        }

    # =========================
    # 📜 GET HISTORY
    # =========================
    def get_history(self):
        with self._connect() as conn:
            cursor = conn.execute("""
            SELECT original_path, backup_path, timestamp
            FROM versions
            ORDER BY timestamp DESC
            """)
            return cursor.fetchall()