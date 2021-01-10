from typing import Any, Dict

from fastapi import APIRouter

from aopi.routes.api import auth_router, packages_router
from aopi.settings import settings

api_router = APIRouter()
api_router.include_router(packages_router, tags=["packages"])
if settings.enable_users:
    api_router.include_router(auth_router, prefix="/auth", tags=["auth"])


@api_router.get("/system", tags=["system"])
def get_backend_info() -> Dict[str, Any]:
    """
    # Get current backend configuration.

    This route is used by frontend application.
    """
    return {"users_enabled": settings.enable_users}
