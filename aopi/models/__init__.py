import sqlalchemy

from aopi.models.meta import database, metadata

__all__ = [
    "create_db",
    "database",
]


def create_db() -> None:
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
