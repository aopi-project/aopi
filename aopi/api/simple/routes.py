import os
import shutil
from operator import attrgetter
from pathlib import Path
from typing import Any, Dict, List, Optional, Union

import aiohttp_jinja2
import ujson
from aiofile import async_open
from aiohttp import web
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp.web_request import FileField
from aiohttp.web_routedef import RouteTableDef
from aiohttp.web_urldispatcher import View
from loguru import logger
from natsort import natsorted

from aopi.api.simple.models import PackageUploadModel, PackageVersion
from aopi.application.view import BaseView
from aopi.settings import settings

router = RouteTableDef()
PREFIX = "/simple"


@router.view(PREFIX)
class PackageUploadView(BaseView):
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
    async def update_readme(version_dir: Path, description: str) -> None:
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
        packages = []
        for pkg in settings.packages_dir.iterdir():
            packages.append(pkg.name)

        return {
            "prefix": PREFIX,
            "packages": packages,
        }

    async def post(self) -> web.Response:
        upload = PackageUploadModel.from_multidict(await self.request.post())
        version_dir = settings.packages_dir / upload.name / upload.version
        pkg_dir = version_dir / upload.filetype
        if pkg_dir.exists():
            raise HTTPConflict(reason="Distribution already exists.")
        try:
            file_path = pkg_dir / upload.content.filename
            await self.save_file(file_path, upload.content)
            # TODO: Parse readme and save it in version dir
            await self.update_info(version_dir=version_dir, upload=upload)
            await self.update_readme(
                version_dir=version_dir, description=upload.description
            )
        except Exception as e:
            logger.error(e)
            shutil.rmtree(pkg_dir)
            return web.Response(
                status=400, reason="Something went wrong during saving."
            )

        return web.Response(status=201)


@router.view(f"{PREFIX}/{{package_name}}/")
class PackageView(View):
    @staticmethod
    async def get_package_info(version_dir: Path) -> Optional[List[PackageVersion]]:
        info_file = version_dir / "info.json"
        if not info_file.exists():
            return None
        packages = []
        async with async_open(info_file, "r") as f:
            dists_info = ujson.loads(await f.read())
            for dist_name, file_info in dists_info.items():
                packages.append(PackageVersion(**file_info))
        return packages

    @aiohttp_jinja2.template("simple/package_versions.jinja2")
    async def get(self) -> Dict[str, Any]:
        pkg_name = self.request.match_info.get("package_name")
        pkg_dir = settings.packages_dir / pkg_name
        if not os.path.exists(pkg_dir):
            raise HTTPNotFound(reason="Package was not found")
        versions = []
        for version_dir in pkg_dir.iterdir():
            if packages := await self.get_package_info(version_dir):
                versions.extend(packages)

        versions = natsorted(versions, key=attrgetter("version"))
        readme = str()
        if len(versions) > 0:
            last_version = versions[-1].version
            readme_file = pkg_dir / last_version / "README"
            async with async_open(readme_file, "r") as f:
                readme = await f.read()

        return {
            "name": pkg_name,
            "prefix": PREFIX,
            "versions": versions,
            "readme": readme,
            "files_host": f"{self.request.scheme}://{self.request.host}",
        }


@router.view(f"{PREFIX}/files/{{pkg_name}}/{{version}}/{{type}}/{{pkg_file}}")
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
