import sqlalchemy as sa

from aopi.models.meta import Base
from aopi.models.roles import AopiRole
from aopi.models.users import AopiUser


class AopiUserRole(Base):
    user_id = sa.Column(sa.Integer, sa.ForeignKey(AopiUser.id))
    role_id = sa.Column(sa.Integer, sa.ForeignKey(AopiRole.id))

    __table_args__ = (sa.UniqueConstraint(user_id, role_id),)
