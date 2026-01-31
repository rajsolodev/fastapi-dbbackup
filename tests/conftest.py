import pytest
from pathlib import Path

@pytest.fixture
def backup_dir(tmp_path) -> Path:
    """
    Isolated backup directory for each test.
    """
    d = tmp_path / "backups"
    d.mkdir()
    return d

@pytest.fixture
def sqlite_url(tmp_path) -> str:
    db_path = tmp_path / "test.sqlite3"
    return f"sqlite:///{db_path}"

@pytest.fixture
def postgres_url() -> str:
    return "postgresql://user:pass@localhost:5432/dbname"

@pytest.fixture
def mysql_url() -> str:
    return "mysql://user:pass@localhost:3306/dbname"
