import numpy as np
import pandas as pd

from services import recommendation_service


TITLE_COLUMN = "영화제목"
GENRE_COLUMN = "장르"
POSTER_COLUMN = "포스터이미지"


class FakeMatrix:
    def __init__(self, name):
        self.name = name

    def __getitem__(self, index):
        return self.name, index


def fake_linear_kernel(row, matrix):
    scores = {
        "genre": np.array([1.0, 0.8, 0.6, 0.4]),
        "overview": np.array([1.0, 0.05, 0.03, 0.01]),
        "actor": np.array([1.0, 0.04, 0.02, 0.01]),
        "director": np.array([1.0, 0.3, 0.2, 0.1]),
    }

    return scores[matrix.name]


def setup_fake_recommendation_data(monkeypatch):
    movie_df = pd.DataFrame(
        [
            {
                TITLE_COLUMN: "Base Movie",
                GENRE_COLUMN: "Drama",
                POSTER_COLUMN: "base.jpg",
            },
            {
                TITLE_COLUMN: "Movie A",
                GENRE_COLUMN: "Drama",
                POSTER_COLUMN: "a.jpg",
            },
            {
                TITLE_COLUMN: "Movie B",
                GENRE_COLUMN: "Action",
                POSTER_COLUMN: "b.jpg",
            },
            {
                TITLE_COLUMN: "Movie C",
                GENRE_COLUMN: "Comedy",
                POSTER_COLUMN: "c.jpg",
            },
        ]
    )

    movie_index = pd.Series(
        movie_df.index,
        index=movie_df[TITLE_COLUMN],
    )

    db_movies = {
        "Movie A": {"id": 101},
        "Movie B": {"id": 102},
        "Movie C": {"id": 103},
    }

    monkeypatch.setattr(recommendation_service, "movie_df", movie_df)
    monkeypatch.setattr(recommendation_service, "movie_index", movie_index)
    monkeypatch.setattr(recommendation_service, "genre_matrix", FakeMatrix("genre"))
    monkeypatch.setattr(recommendation_service, "overview_matrix", FakeMatrix("overview"))
    monkeypatch.setattr(recommendation_service, "actor_matrix", FakeMatrix("actor"))
    monkeypatch.setattr(recommendation_service, "director_matrix", FakeMatrix("director"))
    monkeypatch.setattr(recommendation_service, "linear_kernel", fake_linear_kernel)
    monkeypatch.setattr(
        recommendation_service,
        "get_movie_by_title",
        lambda title: db_movies.get(title),
    )


def test_recommend_movies_success(monkeypatch):
    setup_fake_recommendation_data(monkeypatch)

    result = recommendation_service.recommend_movies("Base Movie", top_n=2)

    assert result["success"] is True
    assert result["title"] == "Base Movie"
    assert len(result["recommendations"]) == 2

    assert result["recommendations"][0]["id"] == 101
    assert result["recommendations"][0]["title"] == "Movie A"
    assert result["recommendations"][0]["genre"] == "Drama"
    assert result["recommendations"][0]["poster_url"] == "a.jpg"
    assert 0 <= result["recommendations"][0]["match_score"] <= 100

    assert result["recommendations"][1]["id"] == 102
    assert result["recommendations"][1]["title"] == "Movie B"


def test_recommend_movies_returns_empty_when_title_not_found(monkeypatch):
    setup_fake_recommendation_data(monkeypatch)

    result = recommendation_service.recommend_movies("Missing Movie", top_n=2)

    assert result["success"] is False
    assert result["title"] == "Missing Movie"
    assert result["recommendations"] == []
    assert "message" in result


def test_recommend_movies_skips_movie_when_db_movie_not_found(monkeypatch):
    setup_fake_recommendation_data(monkeypatch)

    db_movies = {
        "Movie B": {"id": 102},
        "Movie C": {"id": 103},
    }

    monkeypatch.setattr(
        recommendation_service,
        "get_movie_by_title",
        lambda title: None if title == "Movie A" else db_movies.get(title),
    )

    result = recommendation_service.recommend_movies("Base Movie", top_n=2)

    assert result["success"] is True
    assert result["recommendations"][0]["title"] == "Movie B"
    assert len(result["recommendations"]) == 2


def test_recommend_movies_limits_result_count(monkeypatch):
    setup_fake_recommendation_data(monkeypatch)

    result = recommendation_service.recommend_movies("Base Movie", top_n=1)

    assert result["success"] is True
    assert len(result["recommendations"]) == 1