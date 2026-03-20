ALLOWED_EXTENSIONS = [".xlsx", ".txt", ".csv", ".jpg", ".png"]
IGNORED_EXTENSIONS = [".tmp", ".log"]

def should_include(file_path):
    ext = file_path.suffix.lower()

    if ext in IGNORED_EXTENSIONS:
        return False

    if ALLOWED_EXTENSIONS and ext not in ALLOWED_EXTENSIONS:
        return False

    return True