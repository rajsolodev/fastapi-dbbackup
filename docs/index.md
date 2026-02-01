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

### Database Version Support

| Database | Supported Versions | Requirement |
| --- | --- | --- |
| **PostgreSQL** | All (9.x - 17+) | `pg_dump` client version ≥ Server version |
| **MySQL** | All (5.7, 8.0+) | `mysqldump` client version ≥ Server version |
| **SQLite** | All | No special requirements |

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

`fastapi-dbbackup` works great with Docker. Because it uses native database CLI tools, you must ensure the appropriate clients are installed in your container.

We provide separate guides and Dockerfile examples for each database backend:

- [PostgreSQL Setup](docker.md#postgresql-setup)
- [MySQL Setup](docker.md#mysql-mariadb-setup)
- [SQLite Setup](docker.md#sqlite-setup)

See the full [Docker Usage](docker.md) guide for more details.
