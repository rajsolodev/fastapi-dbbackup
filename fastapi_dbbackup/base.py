from abc import ABC, abstractmethod
from pathlib import Path

class BackupEngine(ABC):
    def __init__(self, db_url: str, output_dir: Path):
        self.db_url = db_url
        self.output_dir = output_dir
        self.output_dir.mkdir(parents=True, exist_ok=True)

    @abstractmethod
    def backup(self) -> Path:
        pass

    @abstractmethod
    def restore(self, backup_path: Path):
        pass
