import os
import time
from datetime import datetime, timedelta
from pathlib import Path
from fastapi_dbbackup.storage.base import StorageBackend

def purge_old_backups(storage: StorageBackend, retention_days: int):
    if retention_days <= 0:
        return

    cutoff = datetime.now() - timedelta(days=retention_days)
    backups = storage.list_backups()

    for backup in backups:
        # Expected format: default-YYYYMMDD-HHMMSS.extension[.gz]
        # We try to extract the date part
        try:
            parts = backup.split("-")
            if len(parts) >= 2:
                date_str = parts[1] # YYYYMMDD
                backup_date = datetime.strptime(date_str, "%Y%m%d")
                if backup_date < cutoff:
                    print(f"Deleting old backup (age): {backup}")
                    storage.delete(backup)
        except (ValueError, IndexError):
            # If filename doesn't match format, skip it
            continue

def purge_max_backups(storage: StorageBackend, max_backups: int):
    if max_backups <= 0:
        return

    backups = storage.list_backups()
    if len(backups) <= max_backups:
        return

    # Sort backups by name (which includes YYYYMMDD-HHMMSS)
    sorted_backups = sorted(backups)
    
    # Identify backups to delete (the oldest ones)
    to_delete = sorted_backups[:-max_backups]

    for backup in to_delete:
        print(f"Deleting old backup (count): {backup}")
        storage.delete(backup)
