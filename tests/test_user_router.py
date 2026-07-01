from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import user_router


def create_test_app():
    app = FastAPI()
    app.include_router(user_router.router)
    return app


def test_signup_endpoint(monkeypatch):
    monkeypatch.setattr(
        user_router,
        "create_user",
        lambda username, email, password: {
            "success": True,
            "message": "created",
        },
    )

    client = TestClient(create_test_app())

    response = client.post(
        "/signup",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "1234",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "created",
    }


def test_login_endpoint(monkeypatch):
    monkeypatch.setattr(
        user_router,
        "login_user",
        lambda email, password: {
            "success": True,
            "message": "login success",
            "user": {
                "id": 1,
                "username": "testuser",
                "email": email,
            },
        },
    )

    client = TestClient(create_test_app())

    response = client.post(
        "/login",
        json={
            "email": "test@example.com",
            "password": "1234",
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "login success",
        "user": {
            "id": 1,
            "username": "testuser",
            "email": "test@example.com",
        },
    }