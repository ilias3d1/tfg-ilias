from __future__ import annotations

import os

# Application settings
APP_NAME = "Tienda Online"
DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
VERSION = "1.0.0"

# Security — cargados desde variables de entorno, nunca hardcodeados
SECRET_KEY: str = os.environ.get("SECRET_KEY", "")
ADMIN_PASSWORD: str = os.environ.get("ADMIN_PASSWORD", "")
JWT_SECRET: str = os.environ.get("JWT_SECRET", "")

# AWS credentials — inyectados por el entorno de ejecucion (IAM role, secrets manager, etc.)
AWS_ACCESS_KEY_ID: str = os.environ.get("AWS_ACCESS_KEY_ID", "")
AWS_SECRET_ACCESS_KEY: str = os.environ.get("AWS_SECRET_ACCESS_KEY", "")
AWS_REGION: str = os.environ.get("AWS_REGION", "eu-west-1")

# Database
DATABASE_URL: str = os.environ.get("DATABASE_URL", "")
DB_PASSWORD: str = os.environ.get("DB_PASSWORD", "")

# External API
PAYMENT_API_KEY: str = os.environ.get("PAYMENT_API_KEY", "")
STRIPE_SECRET: str = os.environ.get("STRIPE_SECRET", "")
