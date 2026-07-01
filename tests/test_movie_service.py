import sys
from contextlib import contextmanager
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "backend"))

from services import movie_service

class FakeCursor:
    def __init__(self, fetchone_values=None, fetchall_value=None):
        self.fetchone_values = fetchone_values or []
        self.fetchall_value = fetchall_value or []
        self.execute_calls = []

    def execute(self, query, params=None):
        self.execute_calls.append((query, params))

    def fetchone(self):
        return self.fetchone_values.pop(0)
    
    def fetchall(self):
        return self.fetchall_value
    
@contextmanager
def fake_db_cursor(cursor):
    yield None, cursor

def test_get_movies_without_keyword(monkeypatch):
    cursor = FakeCursor(
        fetchone_values=[{"total": 2}],
        fetchall_value=[
            {"id": 1, "title": "Movie A"},
            {"id": 2, "title": "Movie B"},
        ],
    )

    monkeypatch.setattr(
        movie_service,
        "get_db_cursor",
        lambda: fake_db_cursor(cursor),
    )

    result = movie_service.get_movies(page=1, size=12)

    assert result["movies"] == [
        {"id": 1, "title": "Movie A"},
        {"id": 2, "title": "Movie B"},
    ]
    assert result["page"] == 1
    assert result["size"] == 12
    assert result["total"] == 2
    assert result["total_pages"] == 1
    assert cursor.execute_calls[0][1] is None
    assert cursor.execute_calls[1][1] == (12, 0)

def test_get_movies_with_keyword(monkeypatch):
    cursor = FakeCursor(
        fetchone_values=[{"total": 1}],
        fetchall_value=[
            {"id": 1, "title": "Inception"},
        ],
    )

    monkeypatch.setattr(
        movie_service,
        "get_db_cursor",
        lambda: fake_db_cursor(cursor),
    )

    result = movie_service.get_movies(keyword="Inception", page=2, size=10)

    assert result["total"] == 1
    assert result["total_pages"] == 1
    assert result["movies"] == [{"id": 1, "title": "Inception"}]
    assert cursor.execute_calls[0][1] == ("%Inception%",)
    assert cursor.execute_calls[1][1] == ("%Inception%", 10, 10)

def test_get_movie_detail(monkeypatch):
    movie = {
        "id": 1,
        "title": "Inception",
        "genre": "SF",
    }
    cursor = FakeCursor(fetchone_values=[movie])

    monkeypatch.setattr(
        movie_service,
        "get_db_cursor",
        lambda: fake_db_cursor(cursor),
    )

    result = movie_service.get_movie_detail(1)

    assert result == movie
    assert cursor.execute_calls[0][1] == (1,)


def test_get_popular_movies_adds_fixed_rating(monkeypatch):
    cursor = FakeCursor(
        fetchall_value=[
            {
                "id": 1,
                "title": "Movie A",
                "genre": "Drama",
                "director": "Director A",
                "actors": "Actor A",
                "release_date": "2020-01-01",
                "poster_url": "poster.jpg",
                "overview": "Overview",
            }
        ]
    )

    monkeypatch.setattr(
        movie_service,
        "get_db_cursor",
        lambda: fake_db_cursor(cursor),
    )

    result = movie_service.get_popular_movies(limit=6)

    assert result[0]["id"] == 1
    assert result[0]["title"] == "Movie A"
    assert result[0]["rating"] == 4.5
    assert cursor.execute_calls[0][1] == (6,)