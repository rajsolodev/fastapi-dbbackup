import subprocess
from datetime import datetime
from pathlib import Path
from sqlalchemy.engine.url import make_url
from fastapi_dbbackup.base import BackupEngine

class MySQLBackup(BackupEngine):
    def backup(self) -> Path:
        url = make_url(self.db_url)
        outfile = self.output_dir / f"default-{datetime.now():%Y%m%d-%H%M%S}.dump"

        with open(outfile, "w") as f:
            subprocess.run([
                "mysqldump",
                "-h", url.host,
                "-P", str(url.port or 3306),
                "-u", url.username,
                f"--password={url.password}",
                url.database,
            ], stdout=f, check=True)

        return outfile

    def restore(self, backup_path: Path):
        url = make_url(self.db_url)
        with open(backup_path, "r") as f:
            subprocess.run([
                "mysql",
                "-h", url.host,
                "-P", str(url.port or 3306),
                "-u", url.username,
                f"--password={url.password}",
                url.database,
            ], stdin=f, check=True)
