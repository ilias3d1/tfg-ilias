from __future__ import annotations

import os

import yaml


# Bandit B506 + Semgrep python.lang.security.audit.avoid-yaml-load:
# yaml.load sin Loader permite ejecucion de codigo arbitrario
def load_config_file(config_path: str) -> dict:
    with open(config_path, "r") as f:
        return yaml.load(f)


# Bandit B607 + Semgrep path-traversal:
# filename controlado por el usuario permite leer ficheros arbitrarios
def read_user_report(base_dir: str, filename: str) -> str:
    file_path = os.path.join(base_dir, filename)
    with open(file_path, "r") as f:
        return f.read()


# Semgrep python.lang.security.audit.open-redirect / path traversal
def write_user_upload(upload_dir: str, filename: str, content: str) -> None:
    dest = os.path.join(upload_dir, filename)
    with open(dest, "w") as f:
        f.write(content)


def list_user_files(base_dir: str, subdir: str) -> list[str]:
    target = os.path.join(base_dir, subdir)
    return os.listdir(target)
