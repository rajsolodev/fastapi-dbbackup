import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file if it exists
load_dotenv(find_dotenv(usecwd=True))

DATABASE_URL = os.getenv("DATABASE_URL")

BACKUP_DIR = Path(os.getenv("DBBACKUP_DIR", "backups"))
COMPRESS = os.getenv("DBBACKUP_COMPRESS", "true").lower() == "true"
STORAGE = os.getenv("DBBACKUP_STORAGE", "local")
RETENTION_DAYS = int(os.getenv("DBBACKUP_RETENTION_DAYS", "0"))
MAX_BACKUPS = int(os.getenv("DBBACKUP_MAX_BACKUPS", "0"))

# S3 Settings
S3_BUCKET = os.getenv("DBBACKUP_S3_BUCKET")
S3_REGION = os.getenv("DBBACKUP_S3_REGION")
S3_PREFIX = os.getenv("DBBACKUP_S3_PREFIX", "")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL is required")
