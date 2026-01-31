# Database Engines

`fastapi-dbbackup` supports PostgreSQL, MySQL, and SQLite.

## PostgreSQL

- **Tool**: Uses `pg_dump` and `pg_restore`.
- **Format**: Custom archive format (`-Fc`) by default.
- **Streaming**: Supported for backups.
- **Security**: Uses `PGPASSWORD` environment variable.
- **Robustness**: Dynamic argument building handles missing host/credentials (supports Trust auth).

## MySQL

- **Tool**: Uses `mysqldump` and `mysql`.
- **Format**: Standard SQL dump.
- **Streaming**: Supported for backups.
- **Security**: Uses `MYSQL_PWD` environment variable.
- **Robustness**: Dynamic argument building handles missing host/credentials (supports Trust auth).

## SQLite

- **Tool**: Uses `sqlite3` CLI or Python `sqlite3.backup` API fallback.
- **Streaming**: Not supported (file-based only).
- **Cleanup**: Temporary local files are automatically deleted after cloud upload.
