from app.db.database import Database
from pathlib import Path


class Stats:
    def __init__(self):
        self.db = Database()

    def get_stats(self):
        history = self.db.get_history()

        total_backups = len(history)
        unique_files = len(set(row[0] for row in history))

        total_size = 0
        for row in history:
            path = Path(row[1])
            if path.exists():
                total_size += path.stat().st_size

        last_backup = history[0][2] if history else "N/A"

        return {
            "total_backups": total_backups,
            "unique_files": unique_files,
            "total_size": total_size,
            "last_backup": last_backup
        }