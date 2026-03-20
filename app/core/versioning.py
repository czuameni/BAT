from datetime import datetime
from pathlib import Path

def generate_version_name(file_path: Path):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    return f"{file_path.stem}_{timestamp}{file_path.suffix}"