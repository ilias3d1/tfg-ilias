from __future__ import annotations

# Application settings
APP_NAME = "Tienda Online"
DEBUG = True
VERSION = "1.0.0"

# Security — Gitleaks: generic-api-key, hardcoded-password
SECRET_KEY = "supersecretkey123!"
ADMIN_PASSWORD = "admin1234"
JWT_SECRET = "jwt-secret-do-not-share-abc987xyz"

# AWS credentials — Gitleaks: aws-access-token
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
AWS_REGION = "eu-west-1"

# Database — SonarQube: hardcoded credentials (S2068)
DATABASE_URL = "postgresql://admin:password123@localhost:5432/tienda_db"
DB_PASSWORD = "P@ssw0rd_db_2024"

# External API
PAYMENT_API_KEY = "sk-live-abc123def456ghi789jkl012mno345"
STRIPE_SECRET = "sk_live_51NxampleKeyForTestingPurposesOnly"
