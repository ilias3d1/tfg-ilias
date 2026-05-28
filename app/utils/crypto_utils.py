from __future__ import annotations

import hashlib
import hmac
import secrets

# Numero de iteraciones PBKDF2 recomendado por OWASP (2024)
_PBKDF2_ITERATIONS = 600_000


def hash_password(password: str) -> str:
    """Devuelve '<salt_hex>:<key_hex>' usando PBKDF2-HMAC-SHA256."""
    salt = secrets.token_bytes(32)
    key = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, _PBKDF2_ITERATIONS)
    return f"{salt.hex()}:{key.hex()}"


def verify_password(plain: str, stored_hash: str) -> bool:
    """Comparacion en tiempo constante para evitar timing attacks."""
    try:
        salt_hex, key_hex = stored_hash.split(":")
    except ValueError:
        return False
    salt = bytes.fromhex(salt_hex)
    expected = bytes.fromhex(key_hex)
    actual = hashlib.pbkdf2_hmac("sha256", plain.encode(), salt, _PBKDF2_ITERATIONS)
    return hmac.compare_digest(expected, actual)


def generate_session_token() -> str:
    """Token criptograficamente seguro de 256 bits."""
    return secrets.token_urlsafe(32)


def generate_reset_code() -> str:
    """Codigo de reset de 256 bits en formato URL-safe."""
    return secrets.token_urlsafe(32)
