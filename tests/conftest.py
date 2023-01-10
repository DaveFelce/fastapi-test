from typing import TYPE_CHECKING, Generator

import pytest

from sqlalchemy_utils import create_database, database_exists, drop_database

from fastapi_test.db.base import Base
from fastapi_test.db.session import SyncSessionMaker, sync_engine
from fastapi_test.models import User

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


@pytest.fixture(scope="session", autouse=True)
def setup_db() -> Generator:
    if sync_engine.url.database != "fastapitest_test":
        raise ValueError(f"Unsafe attempt to recreate database: {sync_engine.url.database}")

    if database_exists(sync_engine.url):
        drop_database(sync_engine.url)
    create_database(sync_engine.url)

    yield

    # At end of all tests, drop the test db
    drop_database(sync_engine.url)


@pytest.fixture(scope="function", autouse=True)
def setup_tables() -> Generator:
    """
    autouse set to True so will be run before each test function, to set up tables
    and tear them down after each test runs
    """
    Base.metadata.create_all(bind=sync_engine)

    yield

    # Drop all tables after each test
    Base.metadata.drop_all(bind=sync_engine)


@pytest.fixture(scope="module")
def main_db_session() -> Generator["Session", None, None]:
    with SyncSessionMaker() as session:
        yield session


@pytest.fixture(scope="function")
def db_session(main_db_session: "Session") -> Generator["Session", None, None]:
    yield main_db_session
    main_db_session.rollback()
    main_db_session.expunge_all()


@pytest.fixture(scope="function")
def user(db_session: "Session") -> User:
    test_user = User(username="test-user", email="testuser@test.com")
    db_session.add(test_user)
    db_session.commit()

    return test_user
