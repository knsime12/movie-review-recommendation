from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import sentiment_router


def create_test_app():
    app = FastAPI()
    app.include_router(sentiment_router.router)
    return app


def test_analyze_endpoint(monkeypatch):
    monkeypatch.setattr(
        sentiment_router,
        "predict_sentiment",
        lambda review: {
            "review": review,
            "sentiment": "긍정",
            "positive_prob": 0.9,
            "expected_rating": 5.0,
            "keywords": ["연기", "스토리"],
        },
    )

    client = TestClient(create_test_app())

    response = client.post(
        "/analyze",
        json={"content": "영화가 정말 좋았다"},
    )

    assert response.status_code == 200
    assert response.json() == {
        "review": "영화가 정말 좋았다",
        "sentiment": "긍정",
        "positive_prob": 0.9,
        "expected_rating": 5.0,
        "keywords": ["연기", "스토리"],
    }