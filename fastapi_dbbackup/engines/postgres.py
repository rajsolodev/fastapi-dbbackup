import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import BinaryIO
from sqlalchemy.engine.url import make_url
from fastapi_dbbackup.base import BackupEngine

class PostgresBackup(BackupEngine):
    def backup(self) -> Path:
        url = make_url(self.db_url)
        outfile = self.output_dir / f"default-{datetime.now():%Y%m%d-%H%M%S}.dump"

        env = os.environ.copy()
        if url.password:
            env["PGPASSWORD"] = url.password

        cmd = ["pg_dump", "-Fc"]
        if url.host:
            cmd.extend(["-h", url.host])
        if url.port:
            cmd.extend(["-p", str(url.port)])
        if url.username:
            cmd.extend(["-U", url.username])
        
        cmd.extend(["-f", str(outfile), url.database])

        subprocess.run(cmd, check=True, env=env)
        return outfile

    def backup_stream(self) -> BinaryIO:
        url = make_url(self.db_url)
        env = os.environ.copy()
        if url.password:
            env["PGPASSWORD"] = url.password

        cmd = ["pg_dump", "-Fc"]
        if url.host:
            cmd.extend(["-h", url.host])
        if url.port:
            cmd.extend(["-p", str(url.port)])
        if url.username:
            cmd.extend(["-U", url.username])
        
        cmd.append(url.database)

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
        return process.stdout

    def restore(self, backup_path: Path):
        url = make_url(self.db_url)
        env = os.environ.copy()
        if url.password:
            env["PGPASSWORD"] = url.password

        cmd = ["pg_restore", "-c"]
        if url.host:
            cmd.extend(["-h", url.host])
        if url.port:
            cmd.extend(["-p", str(url.port)])
        if url.username:
            cmd.extend(["-U", url.username])
        
        cmd.extend(["-d", url.database, str(backup_path)])

        subprocess.run(cmd, check=True, env=env)
