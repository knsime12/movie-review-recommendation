from contextlib import contextmanager

from services import user_service


class FakeConnection:
    def __init__(self):
        self.committed = False

    def commit(self):
        self.committed = True


class FakeCursor:
    def __init__(self, fetchone_value=None):
        self.fetchone_value = fetchone_value
        self.execute_calls = []

    def execute(self, query, params=None):
        self.execute_calls.append((query, params))

    def fetchone(self):
        return self.fetchone_value


@contextmanager
def fake_db_cursor(conn, cursor):
    yield conn, cursor


def test_get_user_by_email(monkeypatch):
    user = {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
        "password": "1234",
        "created_at": "2026-01-01",
    }
    conn = FakeConnection()
    cursor = FakeCursor(fetchone_value=user)

    monkeypatch.setattr(
        user_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )

    result = user_service.get_user_by_email("test@example.com")

    assert result == user
    assert cursor.execute_calls[0][1] == ("test@example.com",)


def test_create_user_success(monkeypatch):
    conn = FakeConnection()
    cursor = FakeCursor()

    monkeypatch.setattr(user_service, "get_user_by_email", lambda email: None)
    monkeypatch.setattr(
        user_service,
        "get_db_cursor",
        lambda: fake_db_cursor(conn, cursor),
    )
    monkeypatch.setattr(
        user_service,
        "hash_password",
        lambda password: "hashed-password",
    )

    result = user_service.create_user(
        username="testuser",
        email="test@example.com",
        password="1234",
    )

    assert result["success"] is True
    assert conn.committed is True
    assert cursor.execute_calls[0][1] == (
        "testuser",
        "test@example.com",
        "hashed-password",
    )


def test_create_user_returns_false_when_email_exists(monkeypatch):
    monkeypatch.setattr(
        user_service,
        "get_user_by_email",
        lambda email: {"id": 1, "email": email},
    )

    result = user_service.create_user(
        username="testuser",
        email="test@example.com",
        password="1234",
    )

    assert result["success"] is False
    assert "message" in result


def test_login_user_success(monkeypatch):
    monkeypatch.setattr(
        user_service,
        "get_user_by_email",
        lambda email: {
            "id": 1,
            "username": "testuser",
            "email": email,
            "password": "1234",
        },
    )
    monkeypatch.setattr(
        user_service,
        "verify_password",
        lambda password, stored: True,
    )

    result = user_service.login_user("test@example.com", "1234")

    assert result["success"] is True
    assert result["user"] == {
        "id": 1,
        "username": "testuser",
        "email": "test@example.com",
    }


def test_login_user_returns_false_when_user_not_found(monkeypatch):
    monkeypatch.setattr(user_service, "get_user_by_email", lambda email: None)

    result = user_service.login_user("missing@example.com", "1234")

    assert result["success"] is False
    assert "message" in result


def test_login_user_returns_false_when_password_is_wrong(monkeypatch):
    monkeypatch.setattr(
        user_service,
        "get_user_by_email",
        lambda email: {
            "id": 1,
            "username": "testuser",
            "email": email,
            "password": "1234",
        },
    )
    monkeypatch.setattr(
        user_service,
        "verify_password",
        lambda password, stored: False,
    )

    result = user_service.login_user("test@example.com", "wrong-password")

    assert result["success"] is False
    assert "message" in result