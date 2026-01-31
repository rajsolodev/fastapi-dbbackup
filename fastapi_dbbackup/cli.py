import argparse
import sys
import os
import gzip
import threading
import shutil
from datetime import datetime
from pathlib import Path
from typing import BinaryIO
from fastapi_dbbackup.config import (
    DATABASE_URL, ENGINE, BACKUP_DIR, COMPRESS, STORAGE, 
    RETENTION_DAYS, MAX_BACKUPS, S3_BUCKET, S3_REGION,
    AWS_S3_ACCESS_KEY_ID, AWS_S3_SECRET_ACCESS_KEY, AWS_S3_ENDPOINT_URL, AWS_S3_DEFAULT_ACL
)
from fastapi_dbbackup.detector import detect_backend
from fastapi_dbbackup.compress import compress, decompress
from fastapi_dbbackup.retention import purge_old_backups, purge_max_backups

from fastapi_dbbackup.engines.sqlite import SQLiteBackup
from fastapi_dbbackup.engines.postgres import PostgresBackup
from fastapi_dbbackup.engines.mysql import MySQLBackup

from fastapi_dbbackup.storage.local import LocalStorage
from fastapi_dbbackup.storage.s3 import S3Storage

ENGINE_MAP = {
    "sqlite": SQLiteBackup,
    "postgresql": PostgresBackup, # detector returns postgresql for urls
    "postgres": PostgresBackup,
    "mysql": MySQLBackup,
}

def get_storage():
    if STORAGE == "s3":
        if not S3_BUCKET:
            print("Error: DBBACKUP_S3_BUCKET or AWS_STORAGE_BUCKET_NAME is required for s3 storage")
            sys.exit(1)
        return S3Storage(
            bucket=S3_BUCKET, 
            region=S3_REGION, 
            prefix=str(BACKUP_DIR),
            access_key=AWS_S3_ACCESS_KEY_ID,
            secret_key=AWS_S3_SECRET_ACCESS_KEY,
            endpoint_url=AWS_S3_ENDPOINT_URL,
            default_acl=AWS_S3_DEFAULT_ACL
        )
    return LocalStorage(BACKUP_DIR)

def get_engine():
    backend = ENGINE
    if backend == "auto":
        backend = detect_backend(DATABASE_URL)
    
    engine_cls = ENGINE_MAP.get(backend)
    if not engine_cls:
        print(f"Error: Unsupported database backend '{backend}'")
        sys.exit(1)
    return engine_cls(DATABASE_URL, BACKUP_DIR)

def cmd_backup(args):
    engine = get_engine()
    storage = get_storage()
    
    print(f"Starting backup for {DATABASE_URL}...")
    
    # Try streaming if not local storage and engine supports it
    stream = None
    if STORAGE != "local":
        stream = engine.backup_stream()
        
    if stream:
        filename = f"default-{datetime.now():%Y%m%d-%H%M%S}.dump"
        if COMPRESS:
            filename += ".gz"
            print("Streaming and compressing backup directly to cloud...")
            # Use os.pipe and a thread for streaming compression
            r, w = os.pipe()
            def compress_worker():
                try:
                    with os.fdopen(w, "wb") as f_out:
                        with gzip.GzipFile(fileobj=f_out, mode="wb") as gz:
                            shutil.copyfileobj(stream, gz)
                finally:
                    stream.close()
            
            t = threading.Thread(target=compress_worker, daemon=True)
            t.start()
            fileobj = os.fdopen(r, "rb")
        else:
            print("Streaming backup directly to cloud...")
            fileobj = stream

        try:
            remote_path = storage.upload_fileobj(fileobj, filename)
        finally:
            fileobj.close()
    else:
        # Fallback to file-based backup (or definitely file-based for local)
        backup_file = engine.backup()

        if COMPRESS:
            print("Compressing backup...")
            backup_file = compress(backup_file)

        print(f"Uploading backup to {STORAGE} storage...")
        remote_path = storage.upload(backup_file)

        # If using non-local storage, delete the temporary local backup file
        if STORAGE != "local" and backup_file.exists():
            print(f"Cleaning up local backup file {backup_file}...")
            backup_file.unlink()

    if RETENTION_DAYS > 0:
        print(f"Purging backups older than {RETENTION_DAYS} days...")
        purge_old_backups(storage, RETENTION_DAYS)

    if MAX_BACKUPS > 0:
        print(f"Limiting backups to latest {MAX_BACKUPS} files...")
        purge_max_backups(storage, MAX_BACKUPS)

    print(f"Backup successful: {remote_path}")

def cmd_restore(args):
    engine = get_engine()
    storage = get_storage()
    
    remote_path = args.filename
    if not remote_path:
        backups = storage.list_backups()
        if not backups:
            print("No backups found to restore.")
            return
        # Use latest backup if none specified
        remote_path = sorted(backups)[-1]
        print(f"No backup specified. Using latest: {remote_path}")

    local_path = BACKUP_DIR / remote_path
    # Ensure backup directory exists before downloading
    local_path.parent.mkdir(parents=True, exist_ok=True)
    
    print(f"Downloading {remote_path}...")
    storage.download(remote_path, local_path)

    temp_path = local_path
    if local_path.suffix == ".gz":
        print("Decompressing backup...")
        temp_path = decompress(local_path)

    print(f"Restoring from {temp_path}...")
    engine.restore(temp_path)
    
    if temp_path != local_path and temp_path.exists():
        temp_path.unlink()

    print("Restore successful.")

def cmd_list(args):
    storage = get_storage()
    backups = storage.list_backups()
    if not backups:
        print("No backups found.")
        return
    
    print(f"Backups in {STORAGE} storage:")
    for b in sorted(backups):
        print(f" - {b}")

def main():
    parser = argparse.ArgumentParser(prog="fastapi-dbbackup", description="FastAPI Database Backup Tool")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")

    # Backup command
    backup_parser = subparsers.add_parser("backup", help="Create a database backup")
    
    # Restore command
    restore_parser = subparsers.add_parser("restore", help="Restore a database from a backup")
    restore_parser.add_argument("filename", nargs="?", help="Specific backup file to restore (defaults to latest)")

    # List command
    list_parser = subparsers.add_parser("list", help="List available backups")

    args = parser.parse_args()

    if args.command == "backup":
        cmd_backup(args)
    elif args.command == "restore":
        cmd_restore(args)
    elif args.command == "list":
        cmd_list(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
