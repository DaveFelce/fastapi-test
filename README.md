# Hello World

## configurations

- create a `local.env` file in the root directory
- add vars as required in `fastapi-test.core.config.Settings`

## running

- `poetry install`

### api run

- `poetry run python asgi.py` or `poetry run uvicorn asgi:app --port=8000`

## testing with curl

- curl http://127.0.0.1:8000/fastapi-test/hello-world -H "Accept: application/json" -H "Authorization: Token {api_token}"

## Docker

- docker build -t fastapi_test .
- docker run -d --name fastapi_test_container -p 8000:8000 fastapi_test

