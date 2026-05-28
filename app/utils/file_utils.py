from __future__ import annotations

import os

import yaml


def _safe_join(base_dir: str, untrusted: str) -> str:
    """
    Resuelve la ruta y verifica que queda dentro de base_dir.
    Lanza ValueError si el resultado escapa del directorio base (path traversal).
    """
    base = os.path.realpath(base_dir)
    candidate = os.path.realpath(os.path.join(base, untrusted))
    # os.sep garantiza que '/var/log/app' no sea prefijo de '/var/log/appX'
    if not candidate.startswith(base + os.sep) and candidate != base:
        raise ValueError("Acceso denegado: ruta fuera del directorio permitido.")
    return candidate


def load_config_file(config_path: str) -> dict:
    """yaml.safe_load no ejecuta constructores Python arbitrarios."""
    with open(config_path, "r") as f:
        return yaml.safe_load(f)


def read_user_report(base_dir: str, filename: str) -> str:
    file_path = _safe_join(base_dir, filename)
    with open(file_path, "r") as f:
        return f.read()


def write_user_upload(upload_dir: str, filename: str, content: str) -> None:
    dest = _safe_join(upload_dir, filename)
    with open(dest, "w") as f:
        f.write(content)


def list_user_files(base_dir: str, subdir: str) -> list[str]:
    target = _safe_join(base_dir, subdir)
    return os.listdir(target)
