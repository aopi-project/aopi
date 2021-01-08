from typing import Any, List, Optional

from aopi_index_builder import (
    PackageVersion,
    PluginFullPackageInfo,
    PluginPackagePreview,
)
from fastapi import APIRouter, HTTPException

from aopi.application.plugin_manager import plugin_manager

packages_router = APIRouter()


@packages_router.get("/languages", response_model=List[str])
async def get_available_languages() -> List[str]:
    return plugin_manager.get_languages()


@packages_router.get("/packages", response_model=List[PluginPackagePreview])
async def find_package(
    page: int = 0,
    name: str = "",
    limit: int = 100,
    language: Optional[str] = None,
) -> List[PluginPackagePreview]:
    user_id = None
    return await plugin_manager.find_package(
        page=page, limit=limit, user_id=user_id, package_name=name, language=language
    )


@packages_router.get("/package", response_model=PluginFullPackageInfo)
async def get_package_info(
    plugin_name: str,
    package_id: Any,
) -> PluginFullPackageInfo:
    user_id = None
    info = await plugin_manager.get_package_info(
        user_id=user_id, plugin_name=plugin_name, package_id=package_id
    )
    if info is None:
        raise HTTPException(status_code=404, detail="Package not found")
    return info


@packages_router.get("/versions", response_model=List[PackageVersion])
async def get_package_versions(
    plugin_name: str, package_id: Any
) -> List[PackageVersion]:
    user_id = None
    return await plugin_manager.get_package_versions(
        user_id=user_id, plugin_name=plugin_name, package_id=package_id
    )
