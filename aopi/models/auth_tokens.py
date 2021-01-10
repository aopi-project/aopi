import sqlalchemy as sa

from aopi.models import AopiUser
from aopi.models.meta import Base


class AuthTokens(Base):
    user_id = sa.Column(sa.Integer(), sa.ForeignKey(AopiUser.id), nullable=False)
    refresh_token = sa.Column(sa.Text(), index=True, nullable=False)
    access_token = sa.Column(sa.Text(), nullable=False)

    @classmethod
    def add(cls, access_token: str, refresh_token: str, user_id: int) -> sa.sql.Insert:
        return cls.insert_query(
            access_token=access_token, refresh_token=refresh_token, user_id=user_id
        )
