from contextlib import contextmanager

from services import review_service


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


def test_create_review_success(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_values=[None], lastrowid=10)

    monkeypatch.setattr(
        review_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = review_service.create_review(
        user_id=1,
        movie_id=2,
        content="This movie was great",
        sentiment="positive",
        positive_prob=0.9,
        expected_rating=4.5,
        keywords=["great", "story"],
    )

    assert result["success"] is True
    assert result["review_id"] == 10
    assert conn.committed is True

    assert cursor.execute_calls[0][1] == (1, 2)
    assert cursor.execute_calls[1][1] == (
        1,
        2,
        "This movie was great",
        "positive",
        0.9,
        4.5,
        '["great", "story"]',
    )


def test_create_review_returns_false_when_user_id_missing():
    result = review_service.create_review(
        user_id=None,
        movie_id=2,
        content="This movie was great",
        sentiment="positive",
        positive_prob=0.9,
        expected_rating=4.5,
    )

    assert result["success"] is False
    assert "message" in result


def test_create_review_returns_false_when_content_is_too_short():
    result = review_service.create_review(
        user_id=1,
        movie_id=2,
        content="bad",
        sentiment="negative",
        positive_prob=0.1,
        expected_rating=1.0,
    )

    assert result["success"] is False
    assert "message" in result


def test_create_review_returns_false_when_review_already_exists(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_values=[{"id": 1}])

    monkeypatch.setattr(
        review_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = review_service.create_review(
        user_id=1,
        movie_id=2,
        content="This movie was great",
        sentiment="positive",
        positive_prob=0.9,
        expected_rating=4.5,
    )

    assert result["success"] is False
    assert conn.committed is False
    assert len(cursor.execute_calls) == 1


def test_get_reviews_by_user_success(monkeypatch):
    reviews = [
        {
            "review_id": 1,
            "user_id": 1,
            "movie_id": 2,
            "content": "Good movie",
            "title": "Movie A",
        }
    ]
    conn = FakeConnection()
    cursor = FakeCursor(fetchall_value=reviews)

    monkeypatch.setattr(
        review_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = review_service.get_reviews_by_user(1)

    assert result["success"] is True
    assert result["reviews"] == reviews
    assert cursor.execute_calls[0][1] == (1,)


def test_delete_review_success(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_values=[{"movie_id": 2}])
    deleted_histories = []

    monkeypatch.setattr(
        review_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )
    monkeypatch.setattr(
        review_service,
        "delete_recommendation_histories",
        lambda user_id, movie_id: deleted_histories.append((user_id, movie_id)),
    )

    result = review_service.delete_review(review_id=10, user_id=1)

    assert result["success"] is True
    assert deleted_histories == [(1, 2)]
    assert conn.committed is True
    assert cursor.execute_calls[0][1] == (10, 1)
    assert cursor.execute_calls[1][1] == (10, 1)


def test_delete_review_returns_false_when_review_not_found(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_values=[None])

    monkeypatch.setattr(
        review_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = review_service.delete_review(review_id=10, user_id=1)

    assert result["success"] is False
    assert conn.committed is False
    assert len(cursor.execute_calls) == 1


def test_check_review_exists_true(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_values=[{"id": 1}])

    monkeypatch.setattr(
        review_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = review_service.check_review_exists(user_id=1, movie_id=2)

    assert result["success"] is True
    assert result["exists"] is True
    assert cursor.execute_calls[0][1] == (1, 2)


def test_check_review_exists_false(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_values=[None])

    monkeypatch.setattr(
        review_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = review_service.check_review_exists(user_id=1, movie_id=2)

    assert result["success"] is True
    assert result["exists"] is False
    assert cursor.execute_calls[0][1] == (1, 2)

def test_get_existing_review_returns_review():
    cursor = FakeCursor(fetchone_values=[{"id": 1}])

    result = review_service._get_existing_review(
        cursor=cursor,
        user_id=1,
        movie_id=2,
    )

    assert result == {"id": 1}
    assert cursor.execute_calls[0][1] == (1, 2)


def test_get_existing_review_returns_none():
    cursor = FakeCursor(fetchone_values=[None])

    result = review_service._get_existing_review(
        cursor=cursor,
        user_id=1,
        movie_id=2,
    )

    assert result is None
    assert cursor.execute_calls[0][1] == (1, 2)