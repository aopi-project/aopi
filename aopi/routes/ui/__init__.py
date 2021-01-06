from fastapi import APIRouter

from aopi.routes.ui.routes import user_router

__all__ = ["ui_router"]

ui_router = APIRouter()
ui_router.include_router(user_router)
