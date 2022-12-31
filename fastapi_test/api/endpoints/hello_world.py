import logging

from typing import Any

from fastapi import APIRouter

logger = logging.getLogger("hello-world")

hello_world_router = APIRouter()


@hello_world_router.get(path="/hello-world")
async def hello_world() -> Any:
    return {"message": "Hello World"}
