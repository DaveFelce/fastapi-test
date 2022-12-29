from fastapi_test.core.config import settings

from . import client, fastapi_test_auth_headers


def test_get_hello_world() -> None:
    resp = client.get(
        f"{settings.API_PREFIX}/hello-world",
        headers=fastapi_test_auth_headers,
    )

    assert resp.status_code == 200
    resp_json = resp.json()
    assert resp_json["message"] == "Hello World"
