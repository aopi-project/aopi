from typing import Dict

from fastapi import APIRouter

api_router = APIRouter()


@api_router.get("/shit")
def test() -> Dict[str, str]:
    return {"a": "b"}
