"""Small helpers shared by the API blueprints."""
from datetime import datetime

from flask import jsonify, request


def error(message, status=400):
    return jsonify(message=message), status


def get_json(*required):
    """Return (data, missing_fields). Strips whitespace from string values."""
    data = request.get_json(silent=True) or {}
    data = {k: v.strip() if isinstance(v, str) else v for k, v in data.items()}
    missing = [f for f in required if data.get(f) in (None, "")]
    return data, missing


def parse_date(value):
    if not value:
        return None
    return datetime.strptime(value, "%Y-%m-%d").date()


def user_to_dict(user):
    return {
        "id": user.id,
        "email": user.email,
        "full_name": user.full_name,
        "qualification": user.qualification,
        "dob": user.dob.isoformat() if user.dob else None,
        "active": user.active,
        "roles": [r.name for r in user.roles],
    }
