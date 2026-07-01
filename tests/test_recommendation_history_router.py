from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import recommendation_history_router


def create_test_app():
    app = FastAPI()
    app.include_router(recommendation_history_router.router)
    return app


def test_user_recommendations_endpoint(monkeypatch):
    monkeypatch.setattr(
        recommendation_history_router,
        "get_recommendations_by_user",
        lambda user_id: {
            "success": True,
            "recommendations": [
                {
                    "id": 1,
                    "user_id": user_id,
                    "title": "Movie A",
                }
            ],
        },
    )

    client = TestClient(create_test_app())

    response = client.get("/users/1/recommendations")

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "recommendations": [
            {
                "id": 1,
                "user_id": 1,
                "title": "Movie A",
            }
        ],
    }


def test_save_recommendation_history_endpoint(monkeypatch):
    monkeypatch.setattr(
        recommendation_history_router,
        "create_recommendation_history",
        lambda user_id, base_movie_id, recommended_movie_id, similarity: {
            "success": True,
            "message": "created",
            "history_id": 10,
        },
    )

    client = TestClient(create_test_app())

    response = client.post(
        "/recommendation-history",
        json={
            "user_id": 1,
            "base_movie_id": 2,
            "recommended_movie_id": 3,
            "similarity": 0.87,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "message": "created",
        "history_id": 10,
    }