import os
import sys

from typing import Any
from urllib.parse import urlparse

from pydantic import BaseSettings, PostgresDsn, validator

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

    SQL_DEBUG: bool = False
    USE_NULL_POOL: bool = False
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = "fastapitest"
    SQLALCHEMY_DATABASE_URI: str = ""
    SQLALCHEMY_DATABASE_URI_ASYNC: str = ""
    DB_CONNECTION_RETRY_TIMES: int = 3

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    @classmethod
    def assemble_db_connection(cls, v: str, values: dict[str, Any]) -> Any:
        if v != "":
            db_uri = v.format(values["POSTGRES_DB"])

        else:
            db_uri = PostgresDsn.build(
                scheme="postgresql",
                user=values.get("POSTGRES_USER"),
                password=values.get("POSTGRES_PASSWORD"),
                host=values.get("POSTGRES_HOST"),
                port=values.get("POSTGRES_PORT"),
                path="/" + values.get("POSTGRES_DB", ""),
            )

        if values["TESTING"]:
            parsed_uri = urlparse(db_uri)
            db_uri = parsed_uri._replace(path=parsed_uri.path + "_test").geturl()

        return db_uri

    @validator("SQLALCHEMY_DATABASE_URI_ASYNC", pre=True)
    @classmethod
    def adapt_db_connection_to_async(cls, v: str, values: dict[str, Any]) -> Any:
        if v != "":
            db_uri = v.format(values["POSTGRES_DB"])
        else:
            db_uri = (
                values["SQLALCHEMY_DATABASE_URI"]
                .replace("postgresql://", "postgresql+asyncpg://")
                .replace("sslmode=", "ssl=")
            )

        return db_uri

    class Config:
        case_sensitive = True
        # env var settings priority ie priority 1 will override priority 2:
        # 1 - env vars already loaded (ie the one passed in by kubernetes)
        # 2 - env vars read from *local.env file
        # 3 - values assigned directly in the Settings class
        env_file = os.path.join(BASE_DIR, "local.env")
        env_file_encoding = "utf-8"


settings = Settings()
