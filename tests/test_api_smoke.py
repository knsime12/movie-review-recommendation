import os
import requests
import pytest


pytestmark = pytest.mark.skipif(
    os.getenv("RUN_SMOKE_TESTS") != "true",
    reason="Smoke tests require a running local server. Set RUN_SMOKE_TESTS=True to run."
)


BASE_URL = os.getenv("BASE_URL", "http://127.0.0.1:8000")


def test_home_page():
    response = requests.get(f"{BASE_URL}/")

    assert response.status_code == 200
    assert "text/html" in response.headers.get("content-type", "")
    assert "CineFeel" in response.text


def test_analyze_api_debug():
    payload = {
        "content": "영상미가 좋고 음악도 훌륭해서 몰입감이 좋았다"
    }

    response = requests.post(f"{BASE_URL}/analyze", json=payload)

    print(response.status_code)
    print(response.text)

    assert response.status_code == 200


def test_recommend_api():
    payload = {
        "movie_title": "인터스텔라",
        "top_n": 5
    }

    response = requests.post(f"{BASE_URL}/recommend", json=payload)

    assert response.status_code == 200

    data = response.json()

    assert "title" in data
    assert "recommendations" in data
    assert isinstance(data["recommendations"], list)
    assert len(data["recommendations"]) <= 5

    for movie in data["recommendations"]:
        assert "id" in movie
        assert "title" in movie
        assert "genre" in movie
        assert "poster_url" in movie
        assert "match_score" in movie

        assert movie["title"] != payload["movie_title"]
        assert 0 <= movie["match_score"] <= 100