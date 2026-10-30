"""Token based authentication using Flask-Security-Too.

Flow:
  1. POST /api/login  -> verify password -> return user.get_auth_token()
  2. Frontend stores token and sends it on every request in the
     'Authentication-Token' header.
  3. @auth_required('token') validates it; @roles_required('admin') does RBAC.
"""
from datetime import datetime

from flask import Blueprint, current_app, jsonify
from flask_security import auth_required, current_user, hash_password, verify_password, roles_required

from ..extensions import db
from ..utils import error, get_json, parse_date, user_to_dict

auth_bp = Blueprint("auth", __name__, url_prefix="/api")


def _datastore():
    return current_app.extensions["security"].datastore


@auth_bp.post("/register")
def register():
    data, missing = get_json("email", "password", "full_name")
    if missing:
        return error(f"Missing fields: {', '.join(missing)}")
    if "@" not in data["email"]:
        return error("Enter a valid email")

    if len(data["password"]) < 6:
        return error("Password must be at least 6 characters")

    ds = _datastore()
    if ds.find_user(email=data["email"].lower()):
        return error("Email already registered", 409)

    try:
        dob = parse_date(data.get("dob"))
    except ValueError:
        return error("dob must be YYYY-MM-DD")

    user = ds.create_user(
        email=data["email"].lower(),
        password=hash_password(data["password"]),  # never store plain text
        full_name=data["full_name"],
        qualification=data.get("qualification"),
        dob=dob,
        roles=["user"],
    )
    db.session.commit()
    return jsonify(message="Registered successfully", user=user_to_dict(user)), 201


@auth_bp.post("/login")
def login():
    data, missing = get_json("email", "password")
    if missing:
        return error("Email and password are required")

    user = _datastore().find_user(email=data["email"].lower())
    if not user or not verify_password(data["password"], user.password):
        return error("Invalid email or password", 401)
    if not user.active:
        return error("Your account is blocked. Contact admin.", 403)

    user.last_visit = datetime.utcnow()
    db.session.commit()
    return jsonify(token=user.get_auth_token(), user=user_to_dict(user))


@auth_bp.post("/logout")
@auth_required("token")
def logout():
    # Tokens are stateless; rotating fs_uniquifier invalidates every token
    # issued to this user (logs out all devices).
    _datastore().set_uniquifier(current_user)
    db.session.commit()
    return jsonify(message="Logged out")


@auth_bp.get("/me")
@auth_required("token")
def me():
    return jsonify(user=user_to_dict(current_user))


@auth_bp.get("/admin/ping")
@auth_required("token")
@roles_required("admin")
def admin_ping():
    """Demo endpoint for RBAC: only admin gets 200, users get 403."""
    return jsonify(message=f"Hello admin {current_user.full_name}")
