# tests/test_sqlite_backup.py
import sqlite3
from fastapi_dbbackup.engines.sqlite import SQLiteBackup

def test_sqlite_backup(sqlite_url, backup_dir):
    engine = SQLiteBackup(sqlite_url, backup_dir)
    backup = engine.backup()

    assert backup.exists()
    assert backup.suffix == ".sqlite3"

def test_sqlite_async_url(tmp_path, backup_dir):
    db_path = tmp_path / "async_test.sqlite3"
    # Create the db file first
    with sqlite3.connect(db_path) as conn:
        conn.execute("CREATE TABLE test (id INTEGER PRIMARY KEY)")
    
    url = f"sqlite+aiosqlite:///{db_path}"
    engine = SQLiteBackup(url, backup_dir)
    backup = engine.backup()

    assert backup.exists()
    assert backup.suffix == ".sqlite3"
