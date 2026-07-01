from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import recommendation_router


def create_test_app():
    app = FastAPI()
    app.include_router(recommendation_router.router)
    return app


def test_recommend_endpoint(monkeypatch):
    monkeypatch.setattr(
        recommendation_router,
        "recommend_movies",
        lambda title, top_n=5: {
            "success": True,
            "title": title,
            "recommendations": [
                {
                    "id": 1,
                    "title": "Movie A",
                    "genre": "Drama",
                    "poster_url": "poster.jpg",
                    "match_score": 90.0,
                }
            ],
        },
    )

    client = TestClient(create_test_app())

    response = client.post(
        "/recommend",
        json={
            "movie_title": "Base Movie",
            "top_n": 1,
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "title": "Base Movie",
        "recommendations": [
            {
                "id": 1,
                "title": "Movie A",
                "genre": "Drama",
                "poster_url": "poster.jpg",
                "match_score": 90.0,
            }
        ],
    }