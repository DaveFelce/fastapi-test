import logging

from fastapi import APIRouter

logger = logging.getLogger("hello-world")

accounts_router = APIRouter()
bpl_operations_router = APIRouter()


@accounts_router.get(path="/hello-world")
async def hello_world():
    return {"message": "Hello World"}
