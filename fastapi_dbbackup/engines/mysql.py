import os
import subprocess
from datetime import datetime
from pathlib import Path
from typing import BinaryIO
from sqlalchemy.engine.url import make_url
from fastapi_dbbackup.base import BackupEngine

class MySQLBackup(BackupEngine):
    def backup(self) -> Path:
        url = make_url(self.db_url)
        outfile = self.output_dir / f"default-{datetime.now():%Y%m%d-%H%M%S}.dump"

        env = os.environ.copy()
        if url.password:
            env["MYSQL_PWD"] = url.password

        cmd = ["mysqldump"]
        if url.host:
            cmd.extend(["-h", url.host])
        if url.port:
            cmd.extend(["-P", str(url.port)])
        if url.username:
            cmd.extend(["-u", url.username])
        
        cmd.append(url.database)

        with open(outfile, "w") as f:
            subprocess.run(cmd, stdout=f, check=True, env=env)

        return outfile

    def backup_stream(self) -> BinaryIO:
        url = make_url(self.db_url)
        env = os.environ.copy()
        if url.password:
            env["MYSQL_PWD"] = url.password

        cmd = ["mysqldump"]
        if url.host:
            cmd.extend(["-h", url.host])
        if url.port:
            cmd.extend(["-P", str(url.port)])
        if url.username:
            cmd.extend(["-u", url.username])
        
        cmd.append(url.database)

        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, env=env)
        return process.stdout

    def restore(self, backup_path: Path):
        url = make_url(self.db_url)
        env = os.environ.copy()
        if url.password:
            env["MYSQL_PWD"] = url.password

        cmd = ["mysql"]
        if url.host:
            cmd.extend(["-h", url.host])
        if url.port:
            cmd.extend(["-P", str(url.port)])
        if url.username:
            cmd.extend(["-u", url.username])
        
        cmd.append(url.database)

        with open(backup_path, "r") as f:
            subprocess.run(cmd, stdin=f, check=True, env=env)
