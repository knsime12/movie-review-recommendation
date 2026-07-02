import bcrypt
import hmac


BCRYPT_PREFIXES = ("$2a$", "$2b$", "$2y$")


def hash_password(password):
    password_bytes = password.encode("utf-8")
    hashed = bcrypt.hashpw(password_bytes, bcrypt.gensalt())

    return hashed.decode("utf-8")


def verify_password(password, stored_password):
    if stored_password.startswith(BCRYPT_PREFIXES):
        return bcrypt.checkpw(
            password.encode("utf-8"),
            stored_password.encode("utf-8"),
        )
    
    # Legacy fallback for users saved before password hashing.
    return hmac.compare_digest(password, stored_password)