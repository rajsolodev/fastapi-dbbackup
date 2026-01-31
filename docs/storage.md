# Storage Backends

`fastapi-dbbackup` supports both local and cloud-based storage.

## Local Storage

By default, backups are stored in the local file system.

- **Directory**: Set via `DBBACKUP_DIR`.
- **Cleanup**: Automatic retention and max backup limits apply locally.

## S3-Compatible Storage

Support for AWS S3 and S3-compatible services like **DigitalOcean Spaces**.

### Direct Streaming

For Postgres and MySQL, the tool uses **streaming uploads**. This means data is piped directly from the database tool to the cloud without ever touching your local disk.

- **Reliability**: Uses S3 multipart uploads for large files.
- **Integrity**: Each chunk is verified via checksums.
- **Efficiency**: Zero temporary disk I/O.

### Configuration Example

To use DigitalOcean Spaces:

```env
DBBACKUP_STORAGE=s3
AWS_S3_ENDPOINT_URL=https://nyc3.digitaloceanspaces.com
AWS_S3_REGION=nyc3
AWS_STORAGE_BUCKET_NAME=my-space-name
AWS_S3_ACCESS_KEY_ID=your-key
AWS_S3_SECRET_ACCESS_KEY=your-secret
```
