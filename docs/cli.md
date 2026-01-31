# CLI Reference

The main command is `fastapi-dbbackup`.

## Commands

### `backup`

Creates a backup of the configured database and uploads it to the configured storage.

```bash
fastapi-dbbackup backup
```

### `restore`

Restores the database from a backup file.

- **Latest Backup**: If no filename is provided, the latest backup from storage is used.
- **Specific Backup**: Pass the filename as an argument.

```bash
# Restore latest
fastapi-dbbackup restore

# Restore specific
fastapi-dbbackup restore default-20260131-220000.dump.gz
```

### `list`

Lists all available backups in the configured storage.

```bash
fastapi-dbbackup list
```
