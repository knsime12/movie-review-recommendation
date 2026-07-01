from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import movie_router


def create_test_app():
    app = FastAPI()
    app.include_router(movie_router.router)
    return app


def test_movies_endpoint(monkeypatch):
    monkeypatch.setattr(
        movie_router,
        "get_movies",
        lambda keyword="", page=1, size=12: {
            "movies": [],
            "page": page,
            "size": size,
            "total": 0,
            "total_pages": 0,
        },
    )

    client = TestClient(create_test_app())

    response = client.get("/movies?keyword=test&page=2&size=5")

    assert response.status_code == 200
    assert response.json() == {
        "movies": [],
        "page": 2,
        "size": 5,
        "total": 0,
        "total_pages": 0,
    }


def test_popular_movies_endpoint(monkeypatch):
    monkeypatch.setattr(
        movie_router,
        "get_popular_movies",
        lambda limit=6: [
            {
                "id": 1,
                "title": "Movie A",
            }
        ],
    )

    client = TestClient(create_test_app())

    response = client.get("/movies/popular?limit=1")

    assert response.status_code == 200
    assert response.json() == [
        {
            "id": 1,
            "title": "Movie A",
        }
    ]


def test_movie_detail_endpoint(monkeypatch):
    monkeypatch.setattr(
        movie_router,
        "get_movie_detail",
        lambda movie_id: {
            "id": movie_id,
            "title": "Movie A",
        },
    )

    client = TestClient(create_test_app())

    response = client.get("/movies/1")

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "title": "Movie A",
    }