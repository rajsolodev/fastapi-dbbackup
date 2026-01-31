from abc import ABC, abstractmethod
from pathlib import Path
from typing import BinaryIO, Optional

class BackupEngine(ABC):
    def __init__(self, db_url: str, output_dir: Path):
        self.db_url = db_url
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def backup(self) -> Path:
        pass

    def backup_stream(self) -> BinaryIO:
        """
        Optional: Start a streaming backup and return a file-like object (stdout).
        Returns None if streaming is not supported by the engine.
        """
        return None

    @abstractmethod
    def restore(self, backup_path: Path):
        pass
