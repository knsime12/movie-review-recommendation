from fastapi import FastAPI
from fastapi.testclient import TestClient

from routers import explanation_router


def create_test_app():
    app = FastAPI()
    app.include_router(explanation_router.router)
    return app


def test_recommendation_explanation_endpoint(monkeypatch):
    monkeypatch.setattr(
        explanation_router,
        "generate_recommendation_explanation",
        lambda request_data: {
            "success": True,
            "summary": "리뷰 감성과 기준 영화 유사도를 바탕으로 추천했습니다.",
            "criteria": [
                "리뷰 키워드는 사용자의 감상 포인트를 설명하는 보조 근거입니다.",
                "추천 영화는 기준 영화와의 유사도를 바탕으로 선정되었습니다.",
                "장르, 줄거리, 배우, 감독 정보를 함께 고려했습니다.",
            ],
        },
    )

    client = TestClient(create_test_app())

    response = client.post(
        "/recommendation-explanation",
        json={
            "review": "스토리가 감동적이고 정말 좋았다",
            "sentiment": "긍정",
            "positive_prob": 0.8,
            "expected_rating": 4,
            "keywords": ["스토리", "감동"],
            "base_movie_title": "인터스텔라",
            "recommendations": [
                {
                    "title": "그래비티",
                    "genre": "SF",
                    "match_score": 87.5,
                }
            ],
        },
    )

    assert response.status_code == 200
    assert response.json() == {
        "success": True,
        "summary": "리뷰 감성과 기준 영화 유사도를 바탕으로 추천했습니다.",
        "criteria": [
            "리뷰 키워드는 사용자의 감상 포인트를 설명하는 보조 근거입니다.",
            "추천 영화는 기준 영화와의 유사도를 바탕으로 선정되었습니다.",
            "장르, 줄거리, 배우, 감독 정보를 함께 고려했습니다.",
        ],
    }