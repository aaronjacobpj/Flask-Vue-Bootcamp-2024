"""Creates the admin user if it does not exist yet. Called every time the app starts."""
from models import db, User


def create_admin(app):
    email = app.config["ADMIN_EMAIL"]
    if User.query.filter_by(email=email).first() is None:
        admin = User(name="Admin", email=email, role="admin")
        admin.set_password(app.config["ADMIN_PASSWORD"])
        db.session.add(admin)
        db.session.commit()
        print(f"Admin created: {email}")
