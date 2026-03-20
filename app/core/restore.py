import shutil
from pathlib import Path

def restore_file(backup_path, original_path):
    Path(original_path).parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(backup_path, original_path)