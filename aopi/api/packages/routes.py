import os
import shutil
from pathlib import Path
from typing import Any, Dict, Optional, Union

import aiohttp_jinja2
import ujson
from aiofile import async_open
from aiohttp import web
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound
from aiohttp.web_request import FileField
from aiohttp.web_routedef import RouteTableDef
from aiohttp.web_urldispatcher import View
from loguru import logger

from aopi.api.packages.models import PackageUploadModel, PackageVersion
from aopi.application.view import BaseView
from aopi.settings import settings

router = RouteTableDef()


@router.view("/")
class PackageUploadView(BaseView):
    @staticmethod
    async def save_file(path: Union[Path, str], file: FileField) -> None:
        target_dir = os.path.dirname(path)
        if not os.path.exists(target_dir):
            os.makedirs(target_dir)
        async with async_open(path, "wb") as f:
            await f.write(file.file.read())

    @aiohttp_jinja2.template("index.jinja2")
    async def get(self) -> Dict[str, Any]:
        packages = []
        for pkg in settings.packages_dir.iterdir():
            packages.append(pkg.name)

        return {
            "packages": packages,
        }

    async def post(self) -> web.Response:
        # TODO: Change package layout to:
        # packages
        # └── package
        #     ├── 0.1.1
        #     ├── 0.1.2
        #     ├── 0.1.3
        #     ├── info.json
        #     └── README.(md|rst)
        upload = PackageUploadModel.from_multidict(await self.request.post())
        version_dir = settings.packages_dir / upload.name / upload.version
        pkg_dir = version_dir / upload.filetype
        if pkg_dir.exists():
            raise HTTPConflict(reason="Package already exists.")
        try:
            file_path = pkg_dir / upload.content.filename
            await self.save_file(file_path, upload.content)
            # TODO: Parse readme and save it in version dir
            info_path = pkg_dir / "info.json"
            info_dict = upload.dict(exclude={"content"})
            info_dict["filename"] = str(upload.content.filename)
            async with async_open(info_path, "w") as f:
                await f.write(ujson.dumps(info_dict))
        except Exception as e:
            logger.error(e)
            shutil.rmtree(version_dir)
            return web.Response(
                status=400, reason="Something went wrong during saving."
            )
        logger.debug(
            f"Successfully uploaded {upload.name}:{upload.version}-{upload.filetype}"
        )
        return web.Response(status=201)


@router.view("/{package_name}/")
class PackageView(View):
    @staticmethod
    async def get_package_info(version_dir: Path) -> Optional[PackageVersion]:
        info_file = version_dir / "info.json"
        if not info_file.exists():
            return None
        async with async_open(info_file, "r") as f:
            return PackageVersion(**ujson.loads(await f.read()))

    @aiohttp_jinja2.template("package_versions.jinja2")
    async def get(self) -> Dict[str, Any]:
        pkg_name = self.request.match_info.get("package_name")
        pkg_dir = settings.packages_dir / pkg_name
        if not os.path.exists(pkg_dir):
            raise HTTPNotFound(reason="Package was not found")
        versions = []
        for version_dir in pkg_dir.iterdir():
            for dist_dir in version_dir.iterdir():
                if package := await self.get_package_info(dist_dir):
                    versions.append(package)

        return {
            "name": pkg_name,
            "versions": versions,
            "files_host": f"{self.request.scheme}://{self.request.host}",
        }


@router.view("/packages/{pkg_name}/{version}/{type}/{pkg_file}")
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
