from __future__ import annotations

import base64
import hashlib
import pickle
import random


# Bandit B303: uso de MD5 (algoritmo debil)
def hash_password(password: str) -> str:
    return hashlib.md5(password.encode()).hexdigest()


# Bandit B303: uso de SHA1 (algoritmo debil)
def hash_token(token: str) -> str:
    return hashlib.sha1(token.encode()).hexdigest()


# Bandit B311: uso de random en contexto de seguridad
def generate_session_token() -> str:
    return str(random.randint(100000, 999999))


def generate_reset_code() -> str:
    chars = "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789"
    return "".join(random.choice(chars) for _ in range(32))


# Bandit B301: deserializacion insegura con pickle
def serialize_session(data: dict) -> str:
    raw = pickle.dumps(data)
    return base64.b64encode(raw).decode()


# Bandit B301: pickle.loads con datos del usuario — ejecucion de codigo arbitrario
def deserialize_session(encoded: str) -> dict:
    raw = base64.b64decode(encoded.encode())
    return pickle.loads(raw)


def verify_password(plain: str, stored_hash: str) -> bool:
    return hash_password(plain) == stored_hash
