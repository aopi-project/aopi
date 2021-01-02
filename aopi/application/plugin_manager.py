from typing import Optional

from aopi_index_builder import AopiContextBase, PluginManager
from loguru import logger

from aopi.models import AopiUser, database, metadata
from aopi.models.dict_proxy import DictProxy
from aopi.settings import settings
from aopi.utils.passwords import verify_password


async def get_user_id(username: str, password: str) -> Optional[int]:
    logger.debug(f"{username} trying to connect with {password}")
    query = AopiUser.find(username, AopiUser.id, AopiUser.password)
    user = DictProxy(await database.fetch_one(query))
    if user.is_none():
        return None
    if not await verify_password(user.password, password):
        return None
    return user.id


async def check_user_permission(plugin: str, user_id: int, role: str) -> bool:
    logger.info(f"{plugin}, {user_id}, {role}")
    return True


plugin_manager = PluginManager(
    context=AopiContextBase(
        database=database,
        metadata=metadata,
        main_dir=settings.packages_dir,
        enable_users=settings.enable_users,
        get_user_id_function=get_user_id,
        check_user_permission=check_user_permission,
    )
)
