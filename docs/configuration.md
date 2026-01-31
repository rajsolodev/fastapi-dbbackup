# Configuration

`fastapi-dbbackup` is configuration-driven via environment variables.

## Local Setup

To store backups on your local machine or server, use the following minimal configuration:

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
DBBACKUP_STORAGE=local
# Optional: customize where backups are saved (default: backups/)
DBBACKUP_DIR=my_local_backups
```

## Cloud Setup (S3 / DigitalOcean)

To store backups in the cloud (AWS S3 or DigitalOcean Spaces), use the following configuration:

```env
DATABASE_URL=postgresql://user:pass@localhost:5432/dbname
DBBACKUP_STORAGE=s3
AWS_STORAGE_BUCKET_NAME=your-bucket-name

# Authentication
AWS_S3_ACCESS_KEY_ID=your-access-key
AWS_S3_SECRET_ACCESS_KEY=your-secret-key

# Required for DigitalOcean Spaces or custom S3 providers
AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com
AWS_S3_REGION=nyc3

# Optional: customize the folder/prefix in the bucket
DBBACKUP_DIR=production_backups
```

## Environment Variables Reference

| Variable | Description | Default |
|----------|-------------|---------|
| `DATABASE_URL` | SQLAlchemy-style URL. Required for connection details. Credentials and host are optional if your environment supports it (e.g. Trust auth). | - |
| `DBBACKUP_ENGINE` | Explicit engine selection (`postgres`, `mysql`, `sqlite`, or `auto`) | `auto` |
| `DBBACKUP_DIR` | Local directory for backups or S3 Prefix | `backups` |
| `DBBACKUP_STORAGE` | Storage backend (`local` or `s3`) | `local` |
| `DBBACKUP_COMPRESS` | Enable Gzip compression | `true` |
| `DBBACKUP_RETENTION_DAYS` | Number of days to keep backups (0 = forever) | `0` |
| `DBBACKUP_MAX_BACKUPS` | Maximum number of backups to keep (0 = unlimited) | `0` |

### S3 / DigitalOcean Specifics

| Variable | Description |
|----------|-------------|
| `AWS_S3_ACCESS_KEY_ID` | Your access key ID |
| `AWS_S3_SECRET_ACCESS_KEY` | Your secret access key |
| `AWS_S3_ENDPOINT_URL` | Custom endpoint (Required for DigitalOcean Spaces) |
| `AWS_S3_REGION` | S3 region (e.g., `us-east-1` or `nyc3`) |
| `AWS_STORAGE_BUCKET_NAME` | Bucket or Space name |
| `AWS_S3_DEFAULT_ACL` | File ACL (`private` or `public-read`) |

## Using a .env File

The tool automatically searches for a `.env` file in the current directory and parent directories.

```env
# Example .env
DATABASE_URL=sqlite:///./test.db
DBBACKUP_STORAGE=local
DBBACKUP_RETENTION_DAYS=7
```
