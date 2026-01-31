import gzip
import shutil
from pathlib import Path

def compress(file: Path) -> Path:
    gz_file = file.with_suffix(file.suffix + ".gz")
    with open(file, "rb") as src, gzip.open(gz_file, "wb") as dst:
        shutil.copyfileobj(src, dst)
    file.unlink()
    return gz_file

def decompress(file: Path) -> Path:
    if not file.suffix == ".gz":
        return file
    
    decompressed = file.with_suffix("")
    with gzip.open(file, "rb") as src, open(decompressed, "wb") as dst:
        shutil.copyfileobj(src, dst)
    file.unlink()
    return decompressed
