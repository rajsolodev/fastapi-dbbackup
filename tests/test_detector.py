# tests/test_detector.py
from fastapi_dbbackup.detector import detect_backend

def test_sqlite_detection(sqlite_url):
    assert detect_backend(sqlite_url) == "sqlite"

def test_postgres_detection(postgres_url):
    assert detect_backend(postgres_url) == "postgres"

def test_mysql_detection(mysql_url):
    assert detect_backend(mysql_url) == "mysql"
