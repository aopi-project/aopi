import os
from pathlib import Path
from typing import Optional

import ujson
from aiofile import async_open
from fastapi import UploadFile
from loguru import logger

from aopi.models import PackageUploadModel


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


async def save_file(file_path: Path, target_file: UploadFile) -> None:
    target_dir = os.path.dirname(file_path)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
        logger.debug(file_path)
    await target_file.seek(0)
    async with async_open(file_path, "wb") as dest_file:
        while chunk := await target_file.read(1000):
            await dest_file.write(chunk)
