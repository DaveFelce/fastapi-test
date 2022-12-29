import uvicorn

from fastapi_test import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run("asgi:app", port=8000, reload=False)
