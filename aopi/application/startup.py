from collections import defaultdict

from loguru import logger

from aopi.application.plugin_manager import plugin_manager
from aopi.models import AopiRole, AopiUser
from aopi.models.dict_proxy import DictProxy
from aopi.models.meta import database
from aopi.settings import settings
from aopi.utils.passwords import hash_password


async def connect_db() -> None:
    await database.connect()
    logger.info("Database connected")


async def create_admin() -> None:
    """
    Create admin user if it's not exits.

    """
    hashed_pass = await hash_password("admin")
    find_query = AopiUser.find("admin")
    insert_query = AopiUser.create("admin", hashed_pass)
    if await database.fetch_one(find_query):
        logger.debug("Admin already exists")
        return
    logger.debug("Creating admin")
    await database.execute(insert_query)


async def create_missing_roles() -> None:
    """
    Find missing roles in database and add them.

    :return: nothing
    """
    existing_roles = map(DictProxy, await database.fetch_all(AopiRole.select_query()))
    existing_mapping = defaultdict(list)
    for role in existing_roles:
        existing_mapping[role.plugin_name].append(role.role)
    missing_roles = list()
    for plugin in plugin_manager.plugins_map.values():
        existing_plugin_roles = set(existing_mapping.get(plugin.plugin_name) or [])
        for role in set(plugin.roles) - existing_plugin_roles:
            missing_roles.append({"plugin_name": plugin.plugin_name, "role": role})
    logger.debug(f"Found {len(missing_roles)} missing roles.")
    await database.execute_many(AopiRole.insert_query(), missing_roles)


async def fill_db() -> None:
    """
    Create necessary items on startup.
    Like admin user and missing roles from plugins.

    :return:
    """
    if settings.enable_users:
        await create_admin()
        await create_missing_roles()


async def startup() -> None:
    await connect_db()
    await fill_db()
