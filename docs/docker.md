# Docker Usage

`fastapi-dbbackup` is designed to be highly reliable by using native database CLI tools. When running inside Docker, you must ensure these tools are installed in your container.

## PostgreSQL Setup

To back up a PostgreSQL database, you need the `postgresql-client` package. It is recommended to use a version that matches your database server.

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim-bookworm

# Install PostgreSQL 16 client
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    ca-certificates \
    gnupg \
    && curl -fSsL https://www.postgresql.org/media/keys/ACCC4CF8.asc | gpg --dearmor -o /usr/share/keyrings/postgresql.gpg \
    && echo "deb [signed-by=/usr/share/keyrings/postgresql.gpg] http://apt.postgresql.org/pub/repos/apt/ bookworm-pgdg main" > /etc/apt/sources.list.d/pgdg.list \
    && apt-get update \
    && apt-get install -y --no-install-recommends \
    postgresql-client-16 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Using pyproject.toml or requirements.txt is recommended.
# The packages below are just an example dependency list.
RUN pip install fastapi-dbbackup fastapi[standard] sqlalchemy[asyncio] asyncpg

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### 2. Docker Compose (Full Project)

```yaml
services:
  db:
    image: postgres:16-alpine
    environment:
      POSTGRES_USER: user
      POSTGRES_PASSWORD: password
      POSTGRES_DB: mydb
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U user -d mydb"]
      interval: 5s
      timeout: 5s
      retries: 5

  app:
    build: .
    environment:
      - DATABASE_URL=postgresql+asyncpg://user:password@db:5432/mydb
      - DBBACKUP_ENGINE=postgres
      - DBBACKUP_STORAGE=local
      - DBBACKUP_DIR=dbback
    volumes:
      - .:/app
      - backup_data:/app/dbback
    depends_on:
      db:
        condition: service_healthy

volumes:
  backup_data:
```

---

## MySQL Setup

To back up MySQL or MariaDB, you need the `default-mysql-client` package.

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

# Install MySQL client
RUN apt-get update && apt-get install -y \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Using pyproject.toml or requirements.txt is recommended.
# The packages below are just an example dependency list.
RUN pip install fastapi-dbbackup fastapi[standard] sqlalchemy[asyncio] aiomysql

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### 2. Docker Compose (Full Project)

```yaml
services:
  db:
    image: mysql:8.0
    environment:
      MYSQL_ROOT_PASSWORD: rootpassword
      MYSQL_DATABASE: mydb
      MYSQL_USER: user
      MYSQL_PASSWORD: password
    ports:
      - "3306:3306"
    healthcheck:
      test: ["CMD", "mysqladmin" ,"ping", "-h", "localhost"]
      timeout: 10s
      retries: 5

  app:
    build: .
    environment:
      - DATABASE_URL=mysql+aiomysql://user:password@db:3306/mydb
      - DBBACKUP_ENGINE=mysql
      - DBBACKUP_STORAGE=local
      - DBBACKUP_DIR=dbback
    volumes:
      - .:/app
      - backup_data:/app/dbback
    depends_on:
      db:
        condition: service_healthy

volumes:
  backup_data:
```

---

## SQLite Setup

SQLite is built-in, but the `sqlite3` CLI is recommended for the most reliable backups.

### 1. Dockerfile

```dockerfile
FROM python:3.11-slim

# Install SQLite CLI
RUN apt-get update && apt-get install -y \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . .

# Using pyproject.toml or requirements.txt is recommended.
# The packages below are just an example dependency list.
RUN pip install fastapi-dbbackup fastapi[standard] sqlalchemy[asyncio]

CMD ["uvicorn", "main:app", "--host", "0.0.0.0"]
```

### 2. Docker Compose (Full Project)

```yaml
services:
  app:
    build: .
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./data/mydb.sqlite3
      - DBBACKUP_ENGINE=sqlite
      - DBBACKUP_STORAGE=local
      - DBBACKUP_DIR=dbback
    volumes:
      - .:/app
      - ./data:/app/data
      - backup_data:/app/dbback

volumes:
  backup_data:
```

---

## Usage Tips

### Persistence (Local Storage)

If you are using `DBBACKUP_STORAGE=local`, make sure to mount a volume to your backup directory so that backups are not lost when the container is deleted. This is handled by `backup_data` in the examples above.

### Cloud Storage (Recommended)

For production, we recommend using `DBBACKUP_STORAGE=s3`. This ensures your backups are stored safely outside of your Docker infrastructure.

### Triggering Commands

You can trigger backup or restore manually inside the running container.

#### Backup

```bash
# Standard
docker compose exec app fastapi-dbbackup backup

# Using uv
docker compose exec app uv run fastapi-dbbackup backup
```

#### Restore

```bash
# Standard (restores latest)
docker compose exec app fastapi-dbbackup restore

# Using uv (restores specific file)
docker compose exec app uv run fastapi-dbbackup restore default-20260131-120000.dump.gz
```

### Automating with Crontab

On the host machine, you can add a crontab entry to run the backup daily:

```bash
# Standard
0 3 * * * cd /path/to/project && docker compose exec -T app fastapi-dbbackup backup

# Using uv
0 3 * * * cd /path/to/project && docker compose exec -T app uv run fastapi-dbbackup backup
```
