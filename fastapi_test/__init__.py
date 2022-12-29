from fastapi import FastAPI

from fastapi_test.api.api import api_router
from fastapi_test.core.config import settings
from fastapi_test.version import __version__


def create_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_PREFIX}/openapi.json",
    )
    app.include_router(api_router)

    # Prevent 307 temporary redirects if URLs have slashes on the end
    app.router.redirect_slashes = False

    return app
