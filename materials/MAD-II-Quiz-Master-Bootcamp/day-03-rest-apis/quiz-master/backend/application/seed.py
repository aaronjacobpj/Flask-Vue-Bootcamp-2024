"""Creates tables, roles and the single admin user (admin is never registered)."""
from flask import current_app
from flask_security import hash_password

from .extensions import db


def seed_database():
    datastore = current_app.extensions["security"].datastore
    db.create_all()

    datastore.find_or_create_role(name="admin", description="Quiz Master (superuser)")
    datastore.find_or_create_role(name="user", description="Quiz taker")
    db.session.commit()

    admin_email = current_app.config["ADMIN_EMAIL"]
    if not datastore.find_user(email=admin_email):
        datastore.create_user(
            email=admin_email,
            password=hash_password(current_app.config["ADMIN_PASSWORD"]),
            full_name="Quiz Master",
            roles=["admin"],
        )
        db.session.commit()
