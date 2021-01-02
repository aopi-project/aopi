import sqlalchemy as sa
from sqlalchemy.orm.attributes import InstrumentedAttribute

from aopi.models.meta import Base


class AopiUser(Base):
    username = sa.Column(sa.String(length=255), unique=True, nullable=False)
    password = sa.Column(sa.Text(), nullable=False)

    @classmethod
    def create(cls, username: str, password: str) -> sa.sql.Insert:
        return cls.insert_query(username=username, password=password)

    @classmethod
    def find(cls, username: str, *fields: InstrumentedAttribute) -> sa.sql.Select:
        return cls.select_query(*fields).where(AopiUser.username == username)
