import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    # --- Core ---
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret-change-me")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", "sqlite:///instance.db"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- Flask-Security-Too (token based auth) ---
    SECURITY_PASSWORD_SALT = os.environ.get("SECURITY_PASSWORD_SALT", "dev-salt-change-me")
    SECURITY_PASSWORD_HASH = "bcrypt"
    SECURITY_TOKEN_AUTHENTICATION_HEADER = "Authentication-Token"
    SECURITY_TOKEN_MAX_AGE = 60 * 60 * 24  # token valid for 1 day
    # We build our own JSON login/register endpoints, so CSRF for the
    # token-based API is not needed (no cookies are used for auth).
    WTF_CSRF_ENABLED = False
    SECURITY_CSRF_IGNORE_UNAUTH_ENDPOINTS = True

    # --- Admin seeded on first run ---
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@quizmaster.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")

    # --- CORS (Vite dev server) ---
    FRONTEND_ORIGIN = os.environ.get("FRONTEND_ORIGIN", "http://localhost:5173")
