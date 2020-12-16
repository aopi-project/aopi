import os
import shutil
from operator import attrgetter, itemgetter
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiohttp_jinja2
import sqlalchemy
import ujson
from aiofile import async_open
from aiohttp import web
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp.web_request import FileField
from aiohttp.web_routedef import RouteTableDef
from aiohttp.web_urldispatcher import View
from loguru import logger
from natsort import natsorted
from orm import NoMatch
from sqlalchemy.sql import Select

from aopi import models
from aopi.api.simple.models import PackageUploadModel
from aopi.settings import settings

router = RouteTableDef()
PREFIX = "/simple"


@router.view(PREFIX)
class PackageUploadView(View):
    @staticmethod
    async def save_file(path: Union[Path, str], file: FileField) -> None:
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        async with async_open(path, "wb") as f:
            await f.write(file.file.read())

    @staticmethod
    async def update_info(version_dir: Path, upload: PackageUploadModel) -> None:
        info_path = version_dir / "info.json"
        info_dict = {}
        if info_path.exists():
            async with async_open(info_path, "r") as f:
                info_dict = ujson.loads(await f.read())
        dist_info = upload.dict(exclude={"content"})
        dist_info["filename"] = str(upload.content.filename)
        info_dict[upload.filetype] = dist_info
        async with async_open(info_path, "w") as f:
            await f.write(ujson.dumps(info_dict))

    @staticmethod
    async def update_readme(version_dir: Path, description: Optional[str]) -> None:
        if description is None:
            return
        readme = version_dir / "README"
        if readme.exists():
            async with async_open(readme, "r") as f:
                readme_text = await f.read()
            if readme_text == description:
                return
        async with async_open(readme, "w") as f:
            await f.write(description)

    @aiohttp_jinja2.template("simple/index.jinja2")
    async def get(self) -> Dict[str, Any]:
        select: Select = sqlalchemy.sql.select([models.Package.objects.table.c.name])
        packages = map(itemgetter(0), await models.database.fetch_all(select))
        return {
            "prefix": PREFIX,
            "packages": packages,
        }

    async def post(self) -> web.Response:
        upload = PackageUploadModel.from_multidict(await self.request.post())
        pkg_dir = settings.packages_dir / upload.name / upload.version / upload.filetype
        try:
            await models.PackageVersion.objects.get(
                package__name=upload.name,
                version=upload.version,
                filetype=upload.filetype,
            )
            logger.debug(f"Failed to upload {upload.name}. Already exists.")
            raise HTTPConflict(reason="Distribution already exists.")
        except NoMatch:
            pass
        package_exists = await models.Package.objects.filter(name=upload.name).exists()
        try:
            file_path = pkg_dir / upload.content.filename
            await self.save_file(file_path, upload.content)
            logger.debug(f"Saved package file {upload.name} {upload.filetype}")
            if package_exists:
                package = await models.Package.objects.get(name=upload.name)
                await package.update_by_dist_info(upload)
            else:
                package = await models.Package.create_by_dist_info(upload)
            await models.PackageVersion.create_by_dist_info(
                filename=upload.content.filename,
                package=package,
                size=file_path.stat().st_size,
                dist_info=upload,
            )
        except Exception as e:
            logger.exception(e)
            if pkg_dir.exists():
                shutil.rmtree(pkg_dir)
            return web.Response(
                status=400, reason="Something went wrong during saving."
            )

        return web.Response(status=201)


@router.view(f"{PREFIX}/{{package_name}}/")
class PackageView(View):
    @aiohttp_jinja2.template("simple/package_versions.jinja2")
    async def get(self) -> Dict[str, Any]:
        pkg_name = self.request.match_info.get("package_name")
        versions: List[
            models.PackageVersion
        ] = await models.PackageVersion.objects.filter(package__name=pkg_name).all()
        if not versions:
            raise HTTPNotFound(reason="Package was not found")
        versions = natsorted(versions, key=attrgetter("version"))
        readme = str() if not versions else versions[-1].description
        return {
            "name": pkg_name,
            "prefix": PREFIX,
            "versions": versions,
            "readme": readme,
            "files_host": f"{self.request.scheme}://{self.request.host}",
        }


@router.view("/aopi_files/{pkg_name}/{version}/{type}/{pkg_file}")
class FileView(View):
    async def get(self) -> web.FileResponse:
        path_vars = self.request.match_info
        return web.FileResponse(
            settings.packages_dir
            / path_vars["pkg_name"]
            / path_vars["version"]
            / path_vars["type"]
            / path_vars["pkg_file"],
            status=200,
        )
