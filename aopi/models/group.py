from typing import Optional, Union

import sqlalchemy as sa
from pydantic.main import BaseModel
from sqlalchemy.orm.attributes import InstrumentedAttribute

from aopi.models import AopiUser
from aopi.models.meta import Base


class AopiGroup(Base):
    name = sa.Column(sa.Text(), index=True, nullable=False)
    deletable = sa.Column(sa.Boolean(), nullable=False, default=True)
    created_by = sa.Column(sa.ForeignKey(AopiUser.id), nullable=False)

    @classmethod
    def get_id(cls, group: Union[str, int]) -> Union[int, sa.sql.Select]:
        if isinstance(group, str):
            return cls.select_query(cls.id).where(cls.name == group)
        return group

    @classmethod
    def find(cls, name: str, *fields: InstrumentedAttribute) -> sa.sql.Select:
        return AopiGroup.select_query(*fields).where(cls.name == name)

    @classmethod
    def create(
        cls, *, name: str, deletable: bool, user: Union[str, int]
    ) -> sa.sql.Insert:
        return cls.insert_query(
            name=name, deletable=deletable, created_by=AopiUser.get_id(user)
        )


class AopiGroupModel(BaseModel):
    id: Optional[int]
    name: Optional[str]
    deletable: Optional[bool]
