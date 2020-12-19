from fastapi import APIRouter

from aopi.api.simple import router as package_router

router = APIRouter()
router.include_router(package_router, tags=["simple"])
