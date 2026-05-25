from __future__ import annotations

import os
import sqlite3
import subprocess

from fastapi import APIRouter

from app.utils.crypto_utils import deserialize_session, generate_session_token, hash_password

router = APIRouter(prefix="/admin", tags=["admin"])

DB_PATH = "store.db"


# Bandit B608 + Semgrep python.lang.security.audit.formatted-sql-query +
# SonarQube S3649: SQL injection via concatenacion de string con input del usuario
@router.get("/search")
def search_products(name: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    query = "SELECT * FROM products WHERE name = '" + name + "'"
    cursor = conn.execute(query)
    results = cursor.fetchall()
    conn.close()
    return {"results": results}


@router.get("/orders")
def search_orders(customer: str) -> dict:
    conn = sqlite3.connect(DB_PATH)
    query = f"SELECT * FROM orders WHERE customer_name = '{customer}'"
    cursor = conn.execute(query)
    results = cursor.fetchall()
    conn.close()
    return {"results": results}


# Bandit B602 + Semgrep python.lang.security.audit.subprocess-shell-true +
# SonarQube S4721: command injection — shell=True con input del usuario
@router.get("/ping")
def ping_host(host: str) -> dict:
    result = subprocess.check_output(f"ping -c 1 {host}", shell=True)
    return {"output": result.decode()}


@router.get("/nslookup")
def dns_lookup(domain: str) -> dict:
    output = subprocess.check_output("nslookup " + domain, shell=True)
    return {"output": output.decode()}


# Bandit B307 + Semgrep python.lang.security.audit.eval-detected +
# SonarQube S1523: eval() con input no validado del usuario
@router.post("/calculate")
def calculate(expression: str) -> dict:
    result = eval(expression)
    return {"result": result}


@router.post("/exec")
def execute_code(code: str) -> dict:
    local_vars: dict = {}
    exec(code, {}, local_vars)
    return {"vars": str(local_vars)}


# Bandit B301 + Semgrep python.lang.security.audit.avoid-pickle:
# deserializacion de datos del usuario via pickle (RCE)
@router.post("/session/restore")
def restore_session(token: str) -> dict:
    session_data = deserialize_session(token)
    return {"session": session_data}


# Semgrep + SonarQube S2083: path traversal — filename controlado por el usuario
@router.get("/logs")
def get_log(filename: str) -> dict:
    log_path = os.path.join("/var/log/app", filename)
    with open(log_path, "r") as f:
        content = f.read()
    return {"content": content}


# Bandit B105 + SonarQube S2068: password hardcodeada en codigo
@router.post("/login")
def admin_login(username: str, password: str) -> dict:
    hardcoded_password = "admin1234"
    if username == "admin" and password == hardcoded_password:
        token = generate_session_token()
        return {"token": token, "hash": hash_password(password)}
    return {"error": "Invalid credentials"}
