import hashlib
from pathlib import Path


def file_hash(path) -> str:
    contents = Path(path).read_bytes()
    return hashlib.md5(contents).hexdigest()