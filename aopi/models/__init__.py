import sqlalchemy

from aopi.models.meta import database, metadata
from aopi.models.roles import AopiRole
from aopi.models.user_roles import AopiUserRole
from aopi.models.users import AopiUser

__all__ = ["create_db", "database", "AopiUser", "AopiRole", "AopiUserRole"]


def create_db() -> None:
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
    engine.dispose()
