"""All settings in one place."""
import os


class Config:
    # Used to sign session cookies. Read it from an environment variable in real deployments.
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")

    # A relative SQLite path is created inside the `instance/` folder by Flask-SQLAlchemy.
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///eventhub.db")

    # The admin is created by code on first run. There is no admin sign-up page.
    ADMIN_EMAIL = os.environ.get("ADMIN_EMAIL", "admin@eventhub.com")
    ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD", "admin123")
