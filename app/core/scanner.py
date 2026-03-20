from pathlib import Path
from app.core.filters import should_include

def scan_directory(path: Path):
    files = []

    for file in path.rglob("*"):
        if file.is_file() and should_include(file):
            files.append(file)

    return files