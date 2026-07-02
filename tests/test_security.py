from core.security import hash_password, is_password_hashed, verify_password


def test_hash_password_returns_non_plaintext_value():
    hashed = hash_password("1234")

    assert hashed != "1234"
    assert hashed.startswith("$2")


def test_verify_password_returns_true_for_matching_password():
    hashed = hash_password("1234")

    assert verify_password("1234", hashed) is True


def test_verify_password_returns_false_for_wrong_password():
    hashed = hash_password("1234")

    assert verify_password("wrong-password", hashed) is False


def test_verify_password_supports_legacy_plaintext_password():
    assert verify_password("1234", "1234") is True
    assert verify_password("wrong-password", "1234") is False


def test_is_password_hashed_returns_true_for_bcrypt_hash():
    hashed = hash_password("1234")

    assert is_password_hashed(hashed) is True


def test_is_password_hashed_returns_false_for_plaintext_password():
    assert is_password_hashed("1234") is False