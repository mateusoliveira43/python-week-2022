"""Beerlog configuration."""

from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="BEERLOG",
    load_dotenv=True,
)


def get_database_engine() -> str:
    """
    Get database settings to instantiate a SQLModel engine.

    Returns
    -------
    str
        Database settings.

    """
    if settings.get("DATABASE_SERVER", default="FALSE") != "TRUE":
        return "sqlite:///beerlog.db"

    dialect = "postgresql"
    driver = "psycopg2"
    username = settings.PROJECT_NAME
    password = settings.PROJECT_NAME
    host = settings.DATABASE_HOST
    port = settings.DATABASE_PORT
    database_name = settings.DATABASE_HOST

    return (
        f"{dialect}+{driver}://"
        f"{username}:{password}@{host}:{port}/{database_name}"
    )
