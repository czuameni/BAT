from PySide6.QtCore import QThread, Signal

from app.core.scanner import scan_directory
from app.core.backup_engine import BackupEngine


class BackupWorker(QThread):
    progress = Signal(int, int)
    status = Signal(str)
    finished = Signal(int, int)  # success, errors

    def __init__(self, folder):
        super().__init__()
        self.folder = folder
        self.engine = BackupEngine()

    def run(self):
        self.status.emit("Scanning files...")
        files = scan_directory(self.folder)

        total = len(files)
        current = 0

        success = 0
        errors = 0

        if total == 0:
            self.status.emit("No files to backup")
            self.finished.emit(0, 0)
            return

        self.status.emit("Backing up...")

        for file in files:
            results = self.engine.run_backup([file])

            for _, status, _ in results:
                if status == "backed_up":
                    success += 1
                elif status == "error":
                    errors += 1

            current += 1
            self.progress.emit(current, total)

        self.status.emit(f"Done ({success} files, {errors} errors)")
        self.finished.emit(success, errors)