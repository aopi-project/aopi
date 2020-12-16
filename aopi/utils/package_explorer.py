import asyncio
from pathlib import Path
from typing import Optional

from loguru import logger
from orm import NoMatch
from pkginfo import SDist, Wheel

from aopi import models
from aopi.api.simple.models import DistInfoModel
from aopi.settings import settings


def __get_dist_file(dist_dir: Path, pattern: str) -> Optional[Path]:
    found_files = list(dist_dir.glob(pattern))
    if not found_files:
        return None
    return found_files[0]


async def __inspect_version(version_dir: Path) -> None:
    logger.debug(f"Inspecting version {version_dir.name}")
    for dist_dir in version_dir.iterdir():
        if dist_dir.name == "sdist":
            pattern = "*.tar.gz"
            parser = SDist
        elif dist_dir.name == "bdist_wheel":
            pattern = "*.whl"
            parser = Wheel
        else:
            continue

        file = __get_dist_file(dist_dir, pattern)
        if file is None:
            continue
        info = parser(file).__dict__
        info["filetype"] = dist_dir.name
        dist_info = DistInfoModel(**info)
        try:
            package = await models.Package.objects.get(name=dist_info.name)
            await package.update_by_dist_info(dist_info)
            logger.debug("Updated package info in database")
        except NoMatch:
            package = await models.Package.create_by_dist_info(dist_info)
            logger.debug("Created package record")
        params = dict(
            filename=file.name,
            package=package,
            size=file.stat().st_size,
            dist_info=dist_info,
        )
        try:
            version = await models.PackageVersion.objects.get(
                package=package, filetype=dist_dir.name, version=dist_info.version
            )
            await version.update_by_dist_info(**params)
            logger.debug("Updated version info in database")
        except NoMatch:
            await models.PackageVersion.create_by_dist_info(**params)
            logger.debug("Created package version")


async def __discover_packages() -> None:
    await models.database.connect()
    logger.info("Started package discovering.")
    package_count = 0
    for package_dir in settings.packages_dir.iterdir():
        logger.debug(f"Found {package_dir.name} package")
        for version_dir in package_dir.iterdir():
            await __inspect_version(version_dir)
            package_count += 1
    logger.info(f"Found packages: {package_count}")
    await models.database.disconnect()


def discover_packages() -> None:
    models.create_db()
    loop = asyncio.get_event_loop()
    loop.run_until_complete(__discover_packages())
