import shutil
import subprocess
import sqlite3
from datetime import datetime
from pathlib import Path
from fastapi_dbbackup.base import BackupEngine

class SQLiteBackup(BackupEngine):
    def backup(self) -> Path:
        src_path = self.db_url.replace("sqlite:///", "")
        dest = self.output_dir / f"default-{datetime.now():%Y%m%d-%H%M%S}.sqlite3"

        try:
            # Try CLI first
            subprocess.run(
                ["sqlite3", src_path, f".backup {dest}"],
                check=True,
                capture_output=True
            )
        except (subprocess.CalledProcessError, FileNotFoundError):
            # Fallback to python sqlite3 module
            with sqlite3.connect(src_path) as src_conn:
                dest_conn = sqlite3.connect(str(dest))
                src_conn.backup(dest_conn)
                dest_conn.close()

        return dest

    def restore(self, backup_path: Path):
        dest = self.db_url.replace("sqlite:///", "")
        shutil.copy2(backup_path, dest)
