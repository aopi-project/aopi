from aopi.routes.api.admin.routes import admin_router
from aopi.routes.api.auth import auth_router
from aopi.routes.api.packages.routes import packages_router

__all__ = ["packages_router", "auth_router", "admin_router"]
