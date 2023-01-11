# Hello World

## configurations

- create a `local.env` file in the root directory
- add vars as required in `fastapi-test.core.config.Settings`

## running

- `poetry install`
- `poetry run alembic upgrade head`

### api run

- `poetry run python asgi.py` or `poetry run uvicorn asgi:app --port=8000`

## testing with curl

- `curl -H "Content-Type: application/json" -H "Authorization: Token AUTH_TOKEN" -X POST -d '{"username":"dave","email":"test@test.com"}' http://127.0.0.1:8001/fastapi-test/user`
- `curl http://127.0.0.1:8001/fastapi-test/user/dave -H "Accept: application/json" -H "Authorization: Token AUTH_TOKEN"`

## docker-compose

- `docker-compose -f .docker/development/docker-compose.yml up --build`

the docker container exposes port 8001

