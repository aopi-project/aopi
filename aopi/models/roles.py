import sqlalchemy as sa

from aopi.models.meta import Base


class AopiRole(Base):
    name = sa.Column(sa.String, nullable=False)
    plugin_name = sa.Column(sa.String, nullable=False)
