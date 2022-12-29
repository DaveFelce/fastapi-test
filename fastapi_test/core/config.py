import os
import sys

from typing import Any

from pydantic import BaseSettings, validator

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class Settings(BaseSettings):
    API_PREFIX: str = "/fastapi-test"
    PROJECT_NAME: str = "fastapi-test"
    TESTING: bool = False

    @validator("TESTING")
    @classmethod
    def is_test(cls, v: bool) -> bool:
        command = sys.argv[0]
        args = sys.argv[1:] if len(sys.argv) > 1 else []

        if "pytest" in command or any("test" in arg for arg in args):
            return True
        return v

    FASTAPI_TEST_API_AUTH_TOKEN: str | None = None

    @validator("FASTAPI_TEST_API_AUTH_TOKEN")
    @classmethod
    def fetch_auth_token(cls, v: str | None, values: dict[str, Any]) -> Any:
        if isinstance(v, str) and not values["TESTING"]:
            return v

        if values["TESTING"]:
            return "testing-token"

        return ""

    class Config:
        case_sensitive = True
        # env var settings priority ie priority 1 will override priority 2:
        # 1 - env vars already loaded (ie the one passed in by kubernetes)
        # 2 - env vars read from *local.env file
        # 3 - values assigned directly in the Settings class
        env_file = os.path.join(BASE_DIR, "local.env")
        env_file_encoding = "utf-8"


settings = Settings()
