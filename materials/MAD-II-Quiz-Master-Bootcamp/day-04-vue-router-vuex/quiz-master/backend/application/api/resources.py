"""CRUD APIs for Subjects -> Chapters -> Quizzes -> Questions.

GET  : any logged-in user
POST / PUT / DELETE : admin only
"""
from flask import Blueprint, jsonify
from flask_security import auth_required, roles_required, current_user

from ..extensions import db
from ..models import Subject, Chapter, Quiz, Question
from ..serializers import subject_to_dict, chapter_to_dict, quiz_to_dict, question_to_dict
from ..utils import error, get_json, parse_date

resources_bp = Blueprint("resources", __name__, url_prefix="/api")


def admin_only(fn):
    """Shortcut: token auth + admin role."""
    return auth_required("token")(roles_required("admin")(fn))


# ---------------------------------------------------------------- Subjects
@resources_bp.get("/subjects")
@auth_required("token")
def list_subjects():
    subjects = Subject.query.order_by(Subject.name).all()
    return jsonify([subject_to_dict(s, with_chapters=True) for s in subjects])


@resources_bp.post("/subjects")
@admin_only
def create_subject():
    data, missing = get_json("name")
    if missing:
        return error("Subject name is required")
    if Subject.query.filter_by(name=data["name"]).first():
        return error("Subject already exists", 409)
    s = Subject(name=data["name"], description=data.get("description"))
    db.session.add(s)
    db.session.commit()
    return jsonify(subject_to_dict(s)), 201


@resources_bp.put("/subjects/<int:sid>")
@admin_only
def update_subject(sid):
    s = db.get_or_404(Subject, sid)
    data, missing = get_json("name")
    if missing:
        return error("Subject name is required")
    s.name, s.description = data["name"], data.get("description")
    db.session.commit()
    return jsonify(subject_to_dict(s))


@resources_bp.delete("/subjects/<int:sid>")
@admin_only
def delete_subject(sid):
    db.session.delete(db.get_or_404(Subject, sid))  # cascades to chapters/quizzes
    db.session.commit()
    return jsonify(message="Subject deleted")


# ---------------------------------------------------------------- Chapters
@resources_bp.get("/subjects/<int:sid>/chapters")
@auth_required("token")
def list_chapters(sid):
    subject = db.get_or_404(Subject, sid)
    return jsonify(subject=subject_to_dict(subject),
                   chapters=[chapter_to_dict(c) for c in subject.chapters])


@resources_bp.post("/subjects/<int:sid>/chapters")
@admin_only
def create_chapter(sid):
    db.get_or_404(Subject, sid)
    data, missing = get_json("name")
    if missing:
        return error("Chapter name is required")
    c = Chapter(subject_id=sid, name=data["name"], description=data.get("description"))
    db.session.add(c)
    db.session.commit()
    return jsonify(chapter_to_dict(c)), 201


@resources_bp.put("/chapters/<int:cid>")
@admin_only
def update_chapter(cid):
    c = db.get_or_404(Chapter, cid)
    data, missing = get_json("name")
    if missing:
        return error("Chapter name is required")
    c.name, c.description = data["name"], data.get("description")
    db.session.commit()
    return jsonify(chapter_to_dict(c))


@resources_bp.delete("/chapters/<int:cid>")
@admin_only
def delete_chapter(cid):
    db.session.delete(db.get_or_404(Chapter, cid))
    db.session.commit()
    return jsonify(message="Chapter deleted")


# ---------------------------------------------------------------- Quizzes
@resources_bp.get("/quizzes")
@auth_required("token")
def list_quizzes():
    """All quizzes (used by the user dashboard). Users only see quizzes with questions."""
    quizzes = Quiz.query.order_by(Quiz.date_of_quiz.desc()).all()
    if not current_user.has_role("admin"):
        quizzes = [q for q in quizzes if q.questions]
    return jsonify([quiz_to_dict(q) for q in quizzes])


@resources_bp.get("/chapters/<int:cid>/quizzes")
@auth_required("token")
def list_chapter_quizzes(cid):
    chapter = db.get_or_404(Chapter, cid)
    return jsonify(chapter=chapter_to_dict(chapter),
                   quizzes=[quiz_to_dict(q) for q in chapter.quizzes])


def _quiz_fields(data):
    try:
        duration = int(data.get("time_duration") or 10)
        quiz_date = parse_date(data.get("date_of_quiz"))
    except ValueError:
        return None, "time_duration must be a number and date YYYY-MM-DD"
    if duration <= 0:
        return None, "time_duration must be positive"
    return {"title": data["title"], "time_duration": duration,
            "date_of_quiz": quiz_date, "remarks": data.get("remarks")}, None


@resources_bp.post("/chapters/<int:cid>/quizzes")
@admin_only
def create_quiz(cid):
    db.get_or_404(Chapter, cid)
    data, missing = get_json("title")
    if missing:
        return error("Quiz title is required")
    fields, err = _quiz_fields(data)
    if err:
        return error(err)
    q = Quiz(chapter_id=cid, **{k: v for k, v in fields.items() if v is not None})
    db.session.add(q)
    db.session.commit()
    return jsonify(quiz_to_dict(q)), 201


@resources_bp.put("/quizzes/<int:qid>")
@admin_only
def update_quiz(qid):
    q = db.get_or_404(Quiz, qid)
    data, missing = get_json("title")
    if missing:
        return error("Quiz title is required")
    fields, err = _quiz_fields(data)
    if err:
        return error(err)
    for k, v in fields.items():
        if v is not None:
            setattr(q, k, v)
    db.session.commit()
    return jsonify(quiz_to_dict(q))


@resources_bp.delete("/quizzes/<int:qid>")
@admin_only
def delete_quiz(qid):
    db.session.delete(db.get_or_404(Quiz, qid))
    db.session.commit()
    return jsonify(message="Quiz deleted")


# ---------------------------------------------------------------- Questions
@resources_bp.get("/quizzes/<int:qid>/questions")
@admin_only
def list_questions(qid):
    quiz = db.get_or_404(Quiz, qid)
    return jsonify(quiz=quiz_to_dict(quiz),
                   questions=[question_to_dict(q) for q in quiz.questions])


def _question_fields(data):
    options = data.get("options") or []
    options = [(o or "").strip() for o in options][:4]
    if len([o for o in options if o]) < 2:
        return None, "At least two options are required"
    try:
        correct = int(data.get("correct_option"))
    except (TypeError, ValueError):
        return None, "correct_option must be 1-4"
    if correct < 1 or correct > len(options) or not options[correct - 1]:
        return None, "correct_option must point to a filled option"
    options += [""] * (4 - len(options))
    return {"statement": data["statement"], "option1": options[0], "option2": options[1],
            "option3": options[2] or None, "option4": options[3] or None,
            "correct_option": correct}, None


@resources_bp.post("/quizzes/<int:qid>/questions")
@admin_only
def create_question(qid):
    db.get_or_404(Quiz, qid)
    data, missing = get_json("statement")
    if missing:
        return error("Question statement is required")
    fields, err = _question_fields(data)
    if err:
        return error(err)
    q = Question(quiz_id=qid, **fields)
    db.session.add(q)
    db.session.commit()
    return jsonify(question_to_dict(q)), 201


@resources_bp.put("/questions/<int:qid>")
@admin_only
def update_question(qid):
    q = db.get_or_404(Question, qid)
    data, missing = get_json("statement")
    if missing:
        return error("Question statement is required")
    fields, err = _question_fields(data)
    if err:
        return error(err)
    for k, v in fields.items():
        setattr(q, k, v)
    db.session.commit()
    return jsonify(question_to_dict(q))


@resources_bp.delete("/questions/<int:qid>")
@admin_only
def delete_question(qid):
    db.session.delete(db.get_or_404(Question, qid))
    db.session.commit()
    return jsonify(message="Question deleted")
