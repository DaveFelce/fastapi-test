import logging

from typing import Any

from fastapi import APIRouter, Depends
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from fastapi_test.api.deps import get_session
from fastapi_test.db.base_class import async_run_query
from fastapi_test.enums import HttpErrors
from fastapi_test.models import User
from fastapi_test.schemas import GetUserResponseSchema, PostUserBodySchema

logger = logging.getLogger("user")

user_router = APIRouter()


@user_router.get(
    path="/user/{username}",
    response_model=GetUserResponseSchema,
)
async def get_user(
    username: str,
    db_session: AsyncSession = Depends(get_session),
) -> Any:
    async def _query() -> User:
        return (await db_session.execute(select(User).where(User.username == username))).scalars().first()

    user = await async_run_query(_query, db_session, rollback_on_exc=False)

    if not user:
        raise HttpErrors.NO_USER_FOUND.value

    return user


@user_router.post(
    path="/user",
)
async def post_user(
    payload: PostUserBodySchema,
    db_session: AsyncSession = Depends(get_session),
) -> Any:

    data = payload.dict(exclude_unset=True)
    user = User(username=data["username"], email=data["email"])
    db_session.add(user)
    try:
        await db_session.commit()
    except IntegrityError as exc:
        raise HttpErrors.USER_EXISTS.value from exc

    return {}
