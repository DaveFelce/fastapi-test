from typing import AsyncGenerator

from fastapi import Depends, Header

from fastapi_test.core.config import settings
from fastapi_test.db.session import AsyncSessionMaker
from fastapi_test.enums import HttpErrors


async def get_session() -> AsyncGenerator:
    session = AsyncSessionMaker()
    try:
        yield session
    finally:
        await session.close()


def get_authorization_token(authorization: str = Header(None)) -> str:
    try:
        token_type, token_value = authorization.split(" ")
        if token_type.lower() == "token":
            return token_value
    except (ValueError, AttributeError):
        pass

    raise HttpErrors.INVALID_TOKEN.value


# user as in user of our api, not an account holder.
def user_is_authorised(token: str = Depends(get_authorization_token)) -> None:
    if not token == settings.FASTAPI_TEST_API_AUTH_TOKEN:
        raise HttpErrors.INVALID_TOKEN.value
