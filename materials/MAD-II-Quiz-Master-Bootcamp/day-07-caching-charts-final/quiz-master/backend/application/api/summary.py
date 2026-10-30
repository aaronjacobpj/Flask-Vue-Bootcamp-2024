"""Data for the summary charts.

Results are cached for 60 seconds (cache expiry): charts may be up to a
minute old, but the heavy queries run at most once a minute.
"""
from flask import Blueprint, jsonify
from flask_security import auth_required, roles_required, current_user
from sqlalchemy import func

from ..extensions import db, cache
from ..models import User, Role, Subject, Chapter, Quiz, Score

summary_bp = Blueprint("summary", __name__, url_prefix="/api")

PERCENT = 100.0 * Score.total_scored / Score.total_questions


def _by_subject(*filters):
    """[(subject, attempts, average %, best %)] for scores matching the filters."""
    rows = (db.session.query(Subject.name, func.count(Score.id), func.avg(PERCENT), func.max(PERCENT))
            .join(Chapter, Chapter.subject_id == Subject.id)
            .join(Quiz, Quiz.chapter_id == Chapter.id)
            .join(Score, Score.quiz_id == Quiz.id)
            .filter(Score.total_questions > 0, *filters)
            .group_by(Subject.name).order_by(Subject.name).all())
    return [{"subject": name, "attempts": n, "average": round(avg, 1), "best": round(best, 1)}
            for name, n, avg, best in rows]


@summary_bp.get("/admin/summary")
@auth_required("token")
@roles_required("admin")
@cache.cached(timeout=60, key_prefix="admin_summary")
def admin_summary():
    return jsonify(
        totals={
            "users": User.query.filter(User.roles.any(Role.name == "user")).count(),
            "subjects": Subject.query.count(),
            "quizzes": Quiz.query.count(),
            "attempts": Score.query.count(),
        },
        by_subject=_by_subject(),
    )


@summary_bp.get("/summary")
@auth_required("token")
def user_summary():
    return jsonify(_user_summary(current_user.id))


@cache.memoize(timeout=60)  # cached per user_id
def _user_summary(user_id):
    return {"by_subject": _by_subject(Score.user_id == user_id)}
