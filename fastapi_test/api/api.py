from fastapi import APIRouter, Depends

from fastapi_test.api.deps import user_is_authorised
from fastapi_test.api.endpoints import user
from fastapi_test.core.config import settings

api_router = APIRouter()

api_router.include_router(
    user.user_router,
    prefix=settings.API_PREFIX,
    dependencies=[Depends(user_is_authorised)],
)
