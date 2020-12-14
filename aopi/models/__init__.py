import sqlalchemy

from aopi.models.meta import database, metadata
from aopi.models.user import User

__all__ = ["User", "create_db"]


def create_db() -> None:
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
