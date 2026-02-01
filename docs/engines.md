# Database Engines

`fastapi-dbbackup` supports PostgreSQL, MySQL, and SQLite.

## PostgreSQL

- **Tool**: Uses `pg_dump` and `pg_restore`.
- **Format**: Custom archive format (`-Fc`) by default.
- **Streaming**: Supported for backups.
- **Security**: Uses `PGPASSWORD` environment variable.
- **Robustness**: Dynamic argument building handles missing host/credentials (supports Trust auth).
- **Version Compatibility**: Supports all Postgres versions. Ensure the `pg_dump` client version is equal to or higher than the server version.

## MySQL

- **Tool**: Uses `mysqldump` and `mysql`.
- **Format**: Standard SQL dump.
- **Streaming**: Supported for backups.
- **Security**: Uses `MYSQL_PWD` environment variable.
- **Robustness**: Dynamic argument building handles missing host/credentials (supports Trust auth).
- **Version Compatibility**: Supports all MySQL versions. Ensure the `mysqldump` client version is equal to or higher than the server version.

## SQLite

- **Tool**: Uses `sqlite3` CLI or Python `sqlite3.backup` API fallback.
- **Streaming**: Not supported (file-based only).
- **Cleanup**: Temporary local files are automatically deleted after cloud upload.
