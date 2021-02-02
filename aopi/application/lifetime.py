from collections import defaultdict

from loguru import logger

from aopi.application.plugin_manager import plugin_manager
from aopi.models import AopiRole, AopiUser
from aopi.models.group import AopiGroup
from aopi.models.group_linkage import AopiRoleGroupLinkage, AopiUserGroupLink
from aopi.models.meta import database
from aopi.models.roles import AopiRoleModel
from aopi.settings import settings
from aopi.utils.passwords import hash_password


async def create_admin() -> None:
    """Create admin user if it's not exits."""
    hashed_pass = await hash_password("admin")
    find_query = AopiUser.find("admin")
    insert_query = AopiUser.create("admin", hashed_pass)
    if await database.fetch_one(find_query):
        logger.debug("Admin user already exists")
        return
    logger.debug("Creating admin user")
    await database.execute(insert_query)


async def create_admin_group() -> None:
    """Create admin group if not exists."""
    find_query = AopiGroup.find("admins")
    insert_query = AopiGroup.create(name="admins", deletable=False, user="admin")
    if await database.fetch_one(find_query):
        logger.debug("Admins group already exists")
        return
    logger.debug("Creating admin group")
    await database.execute(insert_query)


async def link_admin_to_admins() -> None:
    """Link admin user to admins group"""
    need_link_query = AopiUserGroupLink.check_user_in_group("admin", "admins")
    link_exists = await database.fetch_val(need_link_query)
    if not link_exists:
        logger.debug("Linking admin to admins group")
        await database.execute(AopiUserGroupLink.link("admin", "admins"))


async def create_missing_roles() -> None:
    """Find missing roles in database and add them."""
    existing_roles = map(
        AopiRoleModel.from_orm, await database.fetch_all(AopiRole.select_query())
    )
    existing_mapping = defaultdict(list)
    for role in existing_roles:
        existing_mapping[role.plugin_name].append(role.role)
    missing_roles = list()
    for plugin in plugin_manager.plugins_map.values():
        existing_plugin_roles = set(existing_mapping.get(plugin.package_name) or [])
        for role in set(plugin.roles) - existing_plugin_roles:
            missing_roles.append({"plugin_name": plugin.package_name, "role": role})
    logger.debug(f"Found {len(missing_roles)} missing roles.")
    await database.execute_many(AopiRole.insert_query(), missing_roles)


async def add_roles_to_admin() -> None:
    """Add all roles from database to admin."""
    group_id = await database.fetch_val(AopiGroup.find("admins", AopiGroup.id))
    roles_in_admin_group = AopiRoleGroupLinkage.roles_in_group(group_id)
    missing_roles = AopiRole.select_query(AopiRole.id).where(
        ~AopiRole.id.in_(roles_in_admin_group)
    )
    roles = [
        {"role_id": role["id"], "group_id": group_id}
        for role in await database.fetch_all(missing_roles)
    ]
    logger.debug(f"Found {len(roles)} missing roles for admin group")
    await database.execute_many(AopiRoleGroupLinkage.insert_query(), roles)


async def fill_db() -> None:
    """Create necessary items on startup."""
    if settings.enable_users:
        await create_admin()
        await create_admin_group()
        await link_admin_to_admins()
        await create_missing_roles()
        await add_roles_to_admin()


async def startup() -> None:
    """Action to perform during startup of the application."""
    await database.connect()
    logger.info("Database connected")
    await fill_db()


async def shutdown() -> None:
    """Actions to perform during shutdown of the application."""
    await database.disconnect()
