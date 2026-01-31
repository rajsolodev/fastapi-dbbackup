import os
from pathlib import Path
from dotenv import load_dotenv, find_dotenv

# Load environment variables from .env file if it exists
load_dotenv(find_dotenv(usecwd=True))

DATABASE_URL = os.getenv("DATABASE_URL")
ENGINE = os.getenv("DBBACKUP_ENGINE", "auto")

BACKUP_DIR = Path(os.getenv("DBBACKUP_DIR", "backups"))
COMPRESS = os.getenv("DBBACKUP_COMPRESS", "true").lower() == "true"
STORAGE = os.getenv("DBBACKUP_STORAGE", "local")
RETENTION_DAYS = int(os.getenv("DBBACKUP_RETENTION_DAYS", "0"))
MAX_BACKUPS = int(os.getenv("DBBACKUP_MAX_BACKUPS", "0"))

# S3 Settings
# New AWS S3 Variable names provided by user
AWS_S3_ACCESS_KEY_ID = os.getenv("AWS_S3_ACCESS_KEY_ID")
AWS_S3_SECRET_ACCESS_KEY = os.getenv("AWS_S3_SECRET_ACCESS_KEY")
AWS_S3_ENDPOINT_URL = os.getenv("AWS_S3_ENDPOINT_URL")
AWS_STORAGE_BUCKET_NAME = os.getenv("AWS_STORAGE_BUCKET_NAME")
AWS_S3_REGION = os.getenv("AWS_S3_REGION")
AWS_S3_DEFAULT_ACL = os.getenv("AWS_S3_DEFAULT_ACL", "private")

# Legacy/Alternative DBBACKUP_S3_* Variables
S3_BUCKET = AWS_STORAGE_BUCKET_NAME or os.getenv("DBBACKUP_S3_BUCKET")
S3_REGION = AWS_S3_REGION or os.getenv("DBBACKUP_S3_REGION")
# BACKUP_DIR is used for both local storage path and S3 prefix

if not DATABASE_URL and ENGINE == "auto":
    raise RuntimeError("DATABASE_URL is required for automatic engine detection. Otherwise, set DBBACKUP_ENGINE.")
