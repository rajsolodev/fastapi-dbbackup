# fastapi-dbbackup

Database-native backup tool for FastAPI and SQLAlchemy. Similar to `django-dbbackup`.

## Features

- **Database Support**: SQLite, PostgreSQL, MySQL.
- **Storage Support**: Local File System, AWS S3, DigitalOcean Spaces.
- **Direct Streaming**: Direct pipe from database to cloud for Postgres/MySQL (No local disk usage).
- **Compression**: Gzip compression supported (including streaming compression).
- **Security**: Secure credential handling via environment variables (no passwords in process lists).
- **Restoration**: Easy database restoration from backups.
- **Retention**: Automatic purging of old backups.
- **CLI**: Intuitive CLI with `backup`, `restore`, and `list` commands.

## Quick Start

1. **Install**:
   ```bash
   pip install fastapi-dbbackup
   ```

2. **Configure**: Create a `.env` file:
   ```env
   DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
   DBBACKUP_STORAGE=s3
   AWS_STORAGE_BUCKET_NAME=my-backups
   ```

3. **Backup**:
   ```bash
   fastapi-dbbackup backup
   ```

## Docker Usage

`fastapi-dbbackup` works great with Docker. Ensure your container has the appropriate database CLI tools installed.

### Example Dockerfile

```dockerfile
FROM python:3.11-slim

# Install database clients (Postgres/MySQL)
RUN apt-get update && apt-get install -y \
    postgresql-client \
    default-mysql-client \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .
RUN pip install fastapi-dbbackup

CMD ["fastapi-dbbackup", "backup"]
```
