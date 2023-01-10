FROM python:3.11 as base

WORKDIR /src
ADD .. .
RUN python -m pip install --upgrade pip
RUN pip install poetry
RUN poetry build

from base as builder

WORKDIR /app
ARG wheel=fastapi_test-*-py3-none-any.whl
COPY --from=base /src/dist/$wheel .
RUN pip install $wheel && rm $wheel
RUN apt update && apt -y install postgresql
CMD ["uvicorn", "asgi:app", "--host", "0.0.0.0", "--port", "8000"]
