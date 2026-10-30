"""Admin-only APIs: manage users, view all scores, search."""
from flask import Blueprint, jsonify, request
from flask_security import auth_required, roles_required

from ..extensions import db
from ..models import User, Role, Subject, Quiz, Score
from ..serializers import subject_to_dict, quiz_to_dict, score_to_dict
from ..utils import user_to_dict, error

admin_bp = Blueprint("admin", __name__, url_prefix="/api/admin")


@auth_required("token")
@roles_required("admin")
def _admin_guard():
    return None


@admin_bp.before_request
def protect():
    """Runs before every route in this blueprint -> whole blueprint is admin only.
    CORS pre-flight (OPTIONS) requests carry no token, so let them through."""
    if request.method == "OPTIONS":
        return None
    return _admin_guard()


@admin_bp.get("/users")
def list_users():
    users = User.query.filter(User.roles.any(Role.name == "user")).order_by(User.full_name).all()
    return jsonify([user_to_dict(u) for u in users])


@admin_bp.patch("/users/<int:uid>/toggle")
def toggle_user(uid):
    user = db.get_or_404(User, uid)
    if user.has_role("admin"):
        return error("Cannot block the admin")
    user.active = not user.active
    db.session.commit()
    return jsonify(user_to_dict(user))


@admin_bp.get("/scores")
def all_scores():
    scores = Score.query.order_by(Score.time_stamp_of_attempt.desc()).all()
    return jsonify([score_to_dict(s) for s in scores])


@admin_bp.get("/search")
def search():
    """/api/admin/search?q=python -> matching users, subjects and quizzes."""
    q = (request.args.get("q") or "").strip()
    if not q:
        return jsonify(users=[], subjects=[], quizzes=[])
    like = f"%{q}%"  # SQLAlchemy escapes this -> safe from SQL injection
    users = User.query.filter(User.roles.any(Role.name == "user"),
                              User.full_name.ilike(like) | User.email.ilike(like)).all()
    subjects = Subject.query.filter(Subject.name.ilike(like)).all()
    quizzes = Quiz.query.filter(Quiz.title.ilike(like)).all()
    return jsonify(users=[user_to_dict(u) for u in users],
                   subjects=[subject_to_dict(s) for s in subjects],
                   quizzes=[quiz_to_dict(z) for z in quizzes])
