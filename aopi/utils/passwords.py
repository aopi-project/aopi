import asyncio
from typing import Any, Callable

from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError

argon_hasher = PasswordHasher()


async def run_async(function: Callable[..., Any], *args: Any) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, function, *args)


async def hash_password(password: str) -> str:
    return await run_async(argon_hasher.hash, password)


async def verify_password(hashed_password: str, password: str) -> bool:
    try:
        return await run_async(argon_hasher.verify, hashed_password, password)
    except VerifyMismatchError:
        return False
