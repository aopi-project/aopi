from typing import Optional, Union

import sqlalchemy as sa
import ujson
from pydantic.main import BaseConfig, BaseModel
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

    @classmethod
    def get_id(cls, user: Union[str, int]) -> Union[int, sa.sql.Select]:
        if isinstance(user, int):
            return user
        return cls.find(user, cls.id)


class AopiUserModel(BaseModel):
    id: Optional[int]
    username: Optional[str]
    password: Optional[str]

    class Config(BaseConfig):
        orm_mode = True
        json_loads = ujson.loads
        json_dumps = ujson.dumps
