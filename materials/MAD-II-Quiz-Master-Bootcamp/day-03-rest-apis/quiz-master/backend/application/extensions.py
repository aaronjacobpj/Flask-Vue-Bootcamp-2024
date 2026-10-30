"""All Flask extensions live here so any module can import them
without causing circular imports (app factory pattern)."""
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security

db = SQLAlchemy()
security = Security()
