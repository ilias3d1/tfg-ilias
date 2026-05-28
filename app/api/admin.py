from __future__ import annotations

import hmac
import os
import re
import sqlite3

from fastapi import APIRouter, HTTPException, status

from app.utils.crypto_utils import generate_session_token, verify_password

router = APIRouter(prefix="/admin", tags=["admin"])

DB_PATH = "store.db"
LOG_BASE = "/var/log/app"

# Patron estricto para nombres de host: letras, digitos, guiones y puntos
_HOST_RE = re.compile(r"^[a-zA-Z0-9.\-]{1,253}$")


# SQL parametrizado — el driver escapa los valores, imposible inyeccion
@router.get("/search")
def search_products(name: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute("SELECT * FROM products WHERE name = ?", (name,))
    results = cursor.fetchall()
    conn.close()
    return {"results": results}


@router.get("/orders")
def search_orders(customer: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.execute(
        "SELECT * FROM orders WHERE customer_name = ?", (customer,)
    )
    results = cursor.fetchall()
    conn.close()
    return {"results": results}


# subprocess sin shell=True y con lista de argumentos — sin interpolacion de shell
@router.get("/ping")
def ping_host(host: str) -> dict:
    if not _HOST_RE.match(host):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nombre de host no valido.",
        )
    import subprocess  # noqa: PLC0415

    result = subprocess.check_output(["ping", "-c", "1", host], shell=False)
    return {"output": result.decode()}


@router.get("/nslookup")
def dns_lookup(domain: str) -> dict:
    if not _HOST_RE.match(domain):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Dominio no valido.",
        )
    import subprocess  # noqa: PLC0415

    output = subprocess.check_output(["nslookup", domain], shell=False)
    return {"output": output.decode()}


# Path traversal resuelto: realpath + verificacion de prefijo
@router.get("/logs")
def get_log(filename: str) -> dict:
    base = os.path.realpath(LOG_BASE)
    log_path = os.path.realpath(os.path.join(base, filename))
    if not log_path.startswith(base + os.sep):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Nombre de fichero no valido.",
        )
    with open(log_path, "r") as f:
        content = f.read()
    return {"content": content}


# Contrasena leida desde variable de entorno; comparacion en tiempo constante
@router.post("/login")
def admin_login(username: str, password: str) -> dict:
    admin_password_hash = os.environ.get("ADMIN_PASSWORD_HASH", "")
    if not admin_password_hash:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="Autenticacion de administrador no configurada.",
        )
    if username == "admin" and verify_password(password, admin_password_hash):
        return {"token": generate_session_token()}
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales invalidas.",
    )
