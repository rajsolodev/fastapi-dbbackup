# tests/test_sqlite_backup.py
import sqlite3
from fastapi_dbbackup.engines.sqlite import SQLiteBackup

def test_sqlite_backup(sqlite_url, backup_dir):
    engine = SQLiteBackup(sqlite_url, backup_dir)
    backup = engine.backup()

    assert backup.exists()
    assert backup.suffix == ".sqlite3"
