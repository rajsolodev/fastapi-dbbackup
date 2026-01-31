import shutil
from pathlib import Path
from typing import List
from fastapi_dbbackup.storage.base import StorageBackend

class LocalStorage(StorageBackend):
    def __init__(self, backup_dir: Path):
        self.backup_dir = backup_dir
        self.backup_dir.mkdir(parents=True, exist_ok=True)

    def upload(self, local_path: Path) -> str:
        if local_path.parent != self.backup_dir:
            dest = self.backup_dir / local_path.name
            shutil.copy2(local_path, dest)
            return local_path.name
        return local_path.name

    def upload_fileobj(self, fileobj: BinaryIO, remote_path: str) -> str:
        dest = self.backup_dir / remote_path
        with open(dest, "wb") as f:
            shutil.copyfileobj(fileobj, f)
        return remote_path

    def download(self, remote_path: str, local_path: Path):
        src = self.backup_dir / remote_path
        if src != local_path:
            shutil.copy2(src, local_path)

    def list_backups(self) -> List[str]:
        return [f.name for f in self.backup_dir.iterdir() if f.is_file()]

    def delete(self, remote_path: str):
        (self.backup_dir / remote_path).unlink(missing_ok=True)
