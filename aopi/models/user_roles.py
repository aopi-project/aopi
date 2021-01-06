from typing import Union

import sqlalchemy as sa
from sqlalchemy import and_, exists
from sqlalchemy.orm.attributes import InstrumentedAttribute

from aopi.models.meta import Base
from aopi.models.roles import AopiRole
from aopi.models.users import AopiUser


class AopiUserRole(Base):
    user_id = sa.Column(sa.Integer, sa.ForeignKey(AopiUser.id))
    role_id = sa.Column(sa.Integer, sa.ForeignKey(AopiRole.id))

    __table_args__ = (sa.UniqueConstraint(user_id, role_id),)

    @classmethod
    def get_user_roles(
        cls, user: Union[str, int], *fields: InstrumentedAttribute
    ) -> sa.sql.Select:
        if isinstance(user, int):
            user_id = user
        else:
            user_id = AopiUser.find(user, AopiUser.id)
        return AopiRole.select_query(*fields).where(
            AopiRole.id.in_(
                cls.select_query(AopiUserRole.role_id).where(
                    AopiUserRole.user_id == user_id
                )
            )
        )

    @classmethod
    def has_role(
        cls, *, user: Union[str, int], plugin_name: str, role: str
    ) -> sa.sql.Select:
        if isinstance(user, int):
            user_id = user
        else:
            user_id = AopiUser.find(user, AopiUser.id)
        role_id = AopiRole.select_query(AopiRole.id).where(
            and_(AopiRole.role == role, AopiRole.plugin_name == plugin_name)
        )
        user_role = cls.select_query(AopiUserRole.id).where(
            and_(AopiUserRole.user_id == user_id, AopiUserRole.role_id == role_id)
        )
        return sa.select([exists(user_role)])
