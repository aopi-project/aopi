from typing import Optional

import sqlalchemy as sa
import ujson
from pydantic.main import BaseConfig, BaseModel
from sqlalchemy import UniqueConstraint

from aopi.models.meta import Base


class AopiRole(Base):
    role = sa.Column(sa.String, nullable=False)
    plugin_name = sa.Column(sa.String, nullable=False)

    __table_args__ = (UniqueConstraint(role, plugin_name),)


class AopiRoleModel(BaseModel):
    id: Optional[int]
    role: Optional[str]
    plugin_name: Optional[str]

    class Config(BaseConfig):
        orm_mode = True
        json_loads = ujson.loads
        json_dumps = ujson.dumps
