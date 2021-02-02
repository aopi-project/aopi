from typing import Union

import sqlalchemy as sa

from aopi.models import AopiRole, AopiUser
from aopi.models.group import AopiGroup
from aopi.models.meta import Base


class AopiUserGroupLink(Base):
    group_id = sa.Column(
        sa.Integer(), sa.ForeignKey(AopiGroup.id), index=True, nullable=False
    )
    user_id = sa.Column(
        sa.Integer(), sa.ForeignKey(AopiUser.id), index=True, nullable=False
    )

    @classmethod
    def get_users_ids_in_group(cls, group: Union[int, str]) -> sa.sql.Select:
        group_id = AopiGroup.get_id(group)
        return cls.select_query(cls.user_id).where(cls.group_id == group_id)

    @classmethod
    def get_user_groups(cls, user: Union[str, int]) -> sa.sql.Select:
        user_id = AopiUser.get_id(user)
        return cls.select_query(cls.group_id).where(cls.user_id == user_id)

    @classmethod
    def link(cls, user: Union[str, int], group: Union[str, int]) -> sa.sql.Insert:
        user_id = AopiUser.get_id(user)
        group_id = AopiGroup.get_id(group)
        return cls.insert_query(group_id=group_id, user_id=user_id)

    @classmethod
    def check_user_in_group(
        cls, user: Union[str, int], group: Union[str, int]
    ) -> sa.sql.Select:
        user_id = AopiUser.get_id(user)
        group_id = AopiGroup.get_id(group)
        return sa.select(
            [
                sa.exists(
                    cls.select_query(cls.id).where(
                        sa.and_(cls.group_id == group_id, cls.user_id == user_id)
                    )
                )
            ]
        )


class AopiRoleGroupLinkage(Base):
    group_id = sa.Column(
        sa.Integer(), sa.ForeignKey(AopiGroup.id), index=True, nullable=False
    )
    role_id = sa.Column(sa.Integer(), sa.ForeignKey(AopiRole.id), nullable=False)

    @classmethod
    def roles_in_group(cls, group: Union[int, str]) -> sa.sql.Select:
        group_id = AopiGroup.get_id(group)
        return cls.select_query(cls.role_id).where(cls.group_id == group_id)

    @classmethod
    def link(cls, group: Union[str, int], role_id: int) -> sa.sql.Insert:
        group_id = AopiGroup.get_id(group)
        return cls.insert_query(group_id=group_id, role_id=role_id)
