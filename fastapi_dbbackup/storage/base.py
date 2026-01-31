from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, BinaryIO

class StorageBackend(ABC):
    @abstractmethod
    def upload(self, local_path: Path) -> str:
        """Upload a file to storage and return its remote path/identifier."""
        pass
    
    @abstractmethod
    def upload_fileobj(self, fileobj: BinaryIO, remote_path: str) -> str:
        """Upload a file-like object to storage and return its remote path/identifier."""
        pass

    @abstractmethod
    def download(self, remote_path: str, local_path: Path):
        """Download a file from storage to a local path."""
        pass

    @abstractmethod
    def list_backups(self) -> List[str]:
        """List all available backups in storage."""
        pass

    @abstractmethod
    def delete(self, remote_path: str):
        """Delete a backup from storage."""
        pass
