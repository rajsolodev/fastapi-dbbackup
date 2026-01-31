import subprocess
from datetime import datetime
from pathlib import Path
from sqlalchemy.engine.url import make_url
from fastapi_dbbackup.base import BackupEngine

class PostgresBackup(BackupEngine):
    def backup(self) -> Path:
        url = make_url(self.db_url)
        outfile = self.output_dir / f"default-{datetime.now():%Y%m%d-%H%M%S}.dump"

        subprocess.run([
            "pg_dump",
            "-Fc",
            "-h", url.host,
            "-p", str(url.port or 5432),
            "-U", url.username,
            "-f", str(outfile),
            url.database,
        ], check=True)

        return outfile

    def restore(self, backup_path: Path):
        url = make_url(self.db_url)
        subprocess.run([
            "pg_restore",
            "-c",  # Clean (drop) database objects before recreating
            "-h", url.host,
            "-p", str(url.port or 5432),
            "-U", url.username,
            "-d", url.database,
            str(backup_path),
        ], check=True)
