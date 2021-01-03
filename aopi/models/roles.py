import sqlalchemy as sa
from sqlalchemy import UniqueConstraint

from aopi.models.meta import Base


class AopiRole(Base):
    role = sa.Column(sa.String, nullable=False)
    plugin_name = sa.Column(sa.String, nullable=False)

    __table_args__ = (UniqueConstraint(role, plugin_name),)
