from pathlib import Path

from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import page_router


def create_test_app():
    app = FastAPI()
    app.include_router(page_router.router)
    return app


def test_api_home_endpoint():
    client = TestClient(create_test_app())

    response = client.get("/api")

    assert response.status_code == 200
    assert response.json() == {
        "message": "CineFeel API is running"
    }


def test_home_endpoint_returns_index_html():
    client = TestClient(create_test_app())

    response = client.get("/")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "CineFeel" in response.text