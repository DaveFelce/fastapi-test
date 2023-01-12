from typing import TYPE_CHECKING

from fastapi import status
from sqlalchemy.future import select

from fastapi_test.core.config import settings
from fastapi_test.models import User

from . import client, fastapi_test_auth_headers

if TYPE_CHECKING:
    from sqlalchemy.orm import Session


def test_get_user(user: User) -> None:
    resp = client.get(
        f"{settings.API_PREFIX}/user/{user.username}",
        headers=fastapi_test_auth_headers,
    )

    assert resp.status_code == status.HTTP_200_OK
    assert resp.json()["email"] == user.email


def test_get_bad_user(user: User) -> None:
    resp = client.get(
        f"{settings.API_PREFIX}/user/badusername",
        headers=fastapi_test_auth_headers,
    )

    assert resp.status_code == status.HTTP_404_NOT_FOUND
    assert resp.json().get("detail").get("display_message") == "User not found for provided name."


def test_post_user(db_session: "Session") -> None:
    username = "test-person"
    email = "testperson@test.com"
    payload = {
        "username": username,
        "email": email,
    }

    resp = client.post(f"{settings.API_PREFIX}/user", json=payload, headers=fastapi_test_auth_headers)
    assert resp.status_code == status.HTTP_200_OK

    user = db_session.execute(select(User).where(User.username == username)).scalar_one()
    assert user.email == email


def test_post_duplicate_user(db_session: "Session", user: User) -> None:
    payload = {
        "username": user.username,
        "email": user.email,
    }

    resp = client.post(f"{settings.API_PREFIX}/user", json=payload, headers=fastapi_test_auth_headers)
    assert resp.status_code == status.HTTP_409_CONFLICT
