import shutil
from pathlib import Path
from app.core.hasher import calculate_hash
from app.core.versioning import generate_version_name
from app.db.database import Database

BACKUP_DIR = Path("data/backups")


class BackupEngine:
    def __init__(self):
        self.db = Database()

    def run_backup(self, files):
        results = []

        for file in files:
            try:
                file_hash = calculate_hash(file)
                existing = self.db.get_file(file)

                if not existing or existing["hash"] != file_hash:
                    backup_path = self._backup_file(file, file_hash)
                    results.append((file, "backed_up", backup_path))
                else:
                    results.append((file, "skipped", None))

            except Exception as e:
                results.append((file, "error", str(e)))

        return results

    def _backup_file(self, file, file_hash):
        version_name = generate_version_name(file)
        destination = BACKUP_DIR / version_name

        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(file, destination)

        self.db.save_version(file, destination, file_hash)

        return destination