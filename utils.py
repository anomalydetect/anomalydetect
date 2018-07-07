from pathlib import Path

def fix_path(base, file_path):

    base = Path(base)
    Path(base / file_path)

    return str(Path(base / file_path).absolute())

