from fastapi.testclient import TestClient

from asgi import app
from fastapi_test.core.config import settings

client = TestClient(app)
fastapi_test_auth_headers = {"Authorization": f"Token {settings.FASTAPI_TEST_API_AUTH_TOKEN}"}
