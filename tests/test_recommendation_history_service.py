from contextlib import contextmanager

from services import recommendation_history_service


class FakeConnection:
    def __init__(self):
        self.committed = False

    def commit(self):
        self.committed = True


class FakeCursor:
    def __init__(self, fetchone_values=None, fetchall_value=None, lastrowid=1):
        self.fetchone_values = fetchone_values or []
        self.fetchall_value = fetchall_value or []
        self.lastrowid = lastrowid
        self.execute_calls = []

    def execute(self, query, params=None):
        self.execute_calls.append((query, params))

    def fetchone(self):
        return self.fetchone_values.pop(0)

    def fetchall(self):
        return self.fetchall_value


@contextmanager
def fake_db_cursor(conn, cursor):
    yield conn, cursor


def test_create_recommendation_history_success(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_values=[None], lastrowid=10)

    monkeypatch.setattr(
        recommendation_history_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = recommendation_history_service.create_recommendation_history(
        user_id=1,
        base_movie_id=2,
        recommended_movie_id=3,
        similarity=0.87,
    )

    assert result["success"] is True
    assert result["history_id"] == 10
    assert conn.committed is True
    assert cursor.execute_calls[0][1] == (1, 2, 3)
    assert cursor.execute_calls[1][1] == (1, 2, 3, 0.87)


def test_create_recommendation_history_returns_false_when_user_id_missing():
    result = recommendation_history_service.create_recommendation_history(
        user_id=None,
        base_movie_id=2,
        recommended_movie_id=3,
        similarity=0.87,
    )

    assert result["success"] is False
    assert "message" in result


def test_create_recommendation_history_returns_false_when_movie_id_missing():
    result = recommendation_history_service.create_recommendation_history(
        user_id=1,
        base_movie_id=None,
        recommended_movie_id=3,
        similarity=0.87,
    )

    assert result["success"] is False
    assert "message" in result


def test_create_recommendation_history_returns_false_when_same_movie():
    result = recommendation_history_service.create_recommendation_history(
        user_id=1,
        base_movie_id=2,
        recommended_movie_id=2,
        similarity=0.87,
    )

    assert result["success"] is False
    assert "message" in result


def test_create_recommendation_history_returns_duplicated_when_history_exists(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_values=[{"id": 1}])

    monkeypatch.setattr(
        recommendation_history_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = recommendation_history_service.create_recommendation_history(
        user_id=1,
        base_movie_id=2,
        recommended_movie_id=3,
        similarity=0.87,
    )

    assert result["success"] is False
    assert result["duplicated"] is True
    assert conn.committed is False
    assert len(cursor.execute_calls) == 1


def test_get_recommendations_by_user_success(monkeypatch):
    recommendations = [
        {
            "id": 1,
            "user_id": 1,
            "base_movie_id": 2,
            "recommended_movie_id": 3,
            "similarity": 0.87,
            "title": "Movie A",
        }
    ]
    conn = FakeConnection()
    cursor = FakeCursor(fetchall_value=recommendations)

    monkeypatch.setattr(
        recommendation_history_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = recommendation_history_service.get_recommendations_by_user(1)

    assert result["success"] is True
    assert result["recommendations"] == recommendations
    assert cursor.execute_calls[0][1] == (1,)


def test_delete_recommendation_histories_success(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor()

    monkeypatch.setattr(
        recommendation_history_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = recommendation_history_service.delete_recommendation_histories(
        user_id=1,
        base_movie_id=2,
    )

    assert result is None
    assert conn.committed is True
    assert cursor.execute_calls[0][1] == (1, 2)