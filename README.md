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

## Installation

```bash
pip install fastapi-dbbackup
```

## Configuration

The tool is configured via environment variables. It automatically loads variables from a `.env` file in your current directory or any parent directory.

| Variable                     | Description                                        | Default     |
| ---------------------------- | -------------------------------------------------- | ----------- |
| `DATABASE_URL`             | SQLAlchemy-style URL. Required for connection details. Credentials and host are optional if your environment supports it (e.g. Trust auth or local sockets). | -           |
| `DBBACKUP_ENGINE`         | Database engine (`postgres`, `mysql`, `sqlite`, or `auto`) | `auto`    |
| `DBBACKUP_DIR`             | Local or Cloud directory for backups              | `backups` |
| `DBBACKUP_STORAGE`         | Storage backend (`local` or `s3`)              | `local`   |
| `DBBACKUP_COMPRESS`        | Whether to compress backups                        | `true`    |
| `DBBACKUP_RETENTION_DAYS`  | Number of days to keep backups (0 = forever)       | `0`       |
| `DBBACKUP_MAX_BACKUPS`     | Maximum number of backups to keep (0 = unlimited)  | `0`       |
| `AWS_S3_ACCESS_KEY_ID`     | AWS/DigitalOcean access key ID                     | -           |
| `AWS_S3_SECRET_ACCESS_KEY` | AWS/DigitalOcean secret access key                 | -           |
| `AWS_S3_ENDPOINT_URL`      | Custom endpoint URL (e.g. for DigitalOcean Spaces) | -           |
| `AWS_S3_REGION`            | S3 region name                                     | -           |
| `AWS_STORAGE_BUCKET_NAME`  | S3 bucket name                                     | -           |
| `AWS_S3_DEFAULT_ACL`       | Uploaded file ACL (`private` or `public-read`) | `private` |

## Usage

### Backup

```bash
fastapi-dbbackup backup
```

### Restore

Restore the latest backup:

```bash
fastapi-dbbackup restore
```

Restore a specific backup:

```bash
fastapi-dbbackup restore default-20260131-120000.dump.gz
```

### List Backups

```bash
fastapi-dbbackup list
```

## Docker Usage

Yes! `fastapi-dbbackup` works great with Docker. However, because it uses native database tools for maximum reliability, you must ensure the appropriate CLI clients are installed in your container.

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

# Your command to run the app or a cron job
CMD ["fastapi-dbbackup", "backup"]
```

### Tips for Docker:

- **Storage**: Use `DBBACKUP_STORAGE=s3` to ensure your backups survive container restarts.
- **Volumes**: If using `local` storage, mount a volume to `DBBACKUP_DIR` (default: `backups`).
- **Database URL**: Ensure your `DATABASE_URL` uses the service name defined in your `docker-compose.yml` (e.g., `postgres://user:pass@db:5432/dbname`).

---

## License

MIT License. See [LICENSE](LICENSE) for details.
