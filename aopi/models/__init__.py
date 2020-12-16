import sqlalchemy

from aopi.models.meta import database, metadata
from aopi.models.package import Package
from aopi.models.package_version import PackageVersion
from aopi.models.user import User

__all__ = ["User", "Package", "PackageVersion", "create_db", "database"]


def create_db() -> None:
    engine = sqlalchemy.create_engine(str(database.url))
    metadata.create_all(engine)
