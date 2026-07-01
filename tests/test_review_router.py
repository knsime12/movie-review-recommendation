from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import review_router


def create_test_app():
    app = FastAPI()
    app.include_router(review_router.router)
    return app


def test_save_review_endpoint(monkeypatch):
    monkeypatch.setattr(
        review_router,
        "create_review",
        lambda user_id, movie_id, content, sentiment, positive_prob, expected_rating, keywords: {
            "success": True,
            "message": "created",
            "review_id": 1,
        },
    )

    client = TestClient(create_test_app())

    response = client.post(
        "/reviews",
        json={
            "user_id": 1,
            "movie_id": 2,
            "content": "좋은 영화였다",
            "sentiment": "긍정",
            "positive_prob": 0.9,
            "expected_rating": 5.0,
            "keywords": ["연기"],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "created",
        "review_id": 1,
    }


def test_user_reviews_endpoint(monkeypatch):
    monkeypatch.setattr(
        review_router,
        "get_reviews_by_user",
        lambda user_id: {
            "success": True,
            "reviews": [
                {
                    "review_id": 1,
                    "user_id": user_id,
                    "content": "좋은 영화였다",
                }
            ],
        },
    )

    client = TestClient(create_test_app())

    response = client.get("/users/1/reviews")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "reviews": [
            {
                "review_id": 1,
                "user_id": 1,
                "content": "좋은 영화였다",
            }
        ],
    }


def test_delete_review_endpoint(monkeypatch):
    monkeypatch.setattr(
        review_router,
        "delete_review",
        lambda review_id, user_id: {
            "success": True,
            "message": "deleted",
        },
    )

    client = TestClient(create_test_app())

    response = client.request(
        "DELETE",
        "/reviews/10",
        json={"user_id": 1},
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "deleted",
    }


def test_check_review_endpoint(monkeypatch):
    monkeypatch.setattr(
        review_router,
        "check_review_exists",
        lambda user_id, movie_id: {
            "success": True,
            "exists": False,
            "message": "available",
        },
    )

    client = TestClient(create_test_app())

    response = client.get("/reviews/check?user_id=1&movie_id=2")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "exists": False,
        "message": "available",
    }