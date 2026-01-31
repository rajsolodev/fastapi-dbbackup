# Installation

`fastapi-dbbackup` can be installed via pip, poetry, or uv.

## Standard Installation

```bash
pip install fastapi-dbbackup
```

## Using with uv (Recommended)

```bash
uv add fastapi-dbbackup
```

## OS Compatibility

- **Linux**: Fully supported (Ubuntu, Debian, CentOS, etc.)
- **Windows**: Fully supported. Ensure database CLI tools are in your PATH.
- **Docker**: Supported. See [Docker Guide](index.md#docker-usage) for details.

## Dependencies

- **SQLAlchemy**: Used for database detection and URL parsing.
- **Boto3**: Required for S3/DigitalOcean cloud storage.
- **Python-Dotenv**: Automatically loads your `.env` configuration.
