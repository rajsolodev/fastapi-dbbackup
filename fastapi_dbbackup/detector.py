from sqlalchemy.engine.url import make_url

def detect_backend(database_url: str) -> str:
    backend = make_url(database_url).get_backend_name()

    if backend == "sqlite":
        return "sqlite"
    if backend.startswith("postgresql"):
        return "postgres"
    if backend.startswith("mysql"):
        return "mysql"

    raise ValueError(f"Unsupported database backend: {backend}")
