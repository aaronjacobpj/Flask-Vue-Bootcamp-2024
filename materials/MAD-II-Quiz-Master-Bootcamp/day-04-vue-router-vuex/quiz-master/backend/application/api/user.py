"""Quiz taking + scores for normal users."""
from flask import Blueprint, jsonify
from flask_security import auth_required, roles_required, current_user

from ..extensions import db
from ..models import Quiz, Score
from ..serializers import quiz_to_dict, question_to_dict, score_to_dict
from ..utils import get_json, error

user_bp = Blueprint("user", __name__, url_prefix="/api")


@user_bp.get("/quizzes/<int:qid>/attempt")
@auth_required("token")
@roles_required("user")
def start_quiz(qid):
    quiz = db.get_or_404(Quiz, qid)
    if not quiz.questions:
        return error("This quiz has no questions yet")
    return jsonify(quiz=quiz_to_dict(quiz),
                   questions=[question_to_dict(q, with_answer=False) for q in quiz.questions])


@user_bp.post("/quizzes/<int:qid>/submit")
@auth_required("token")
@roles_required("user")
def submit_quiz(qid):
    """Body: {"answers": {"<question_id>": <option 1-4>, ...}}
    Score is always computed on the server - never trust the client."""
    quiz = db.get_or_404(Quiz, qid)
    data, _ = get_json()
    answers = data.get("answers") or {}

    correct = 0
    for q in quiz.questions:
        chosen = answers.get(str(q.id))
        if chosen is not None and str(chosen) == str(q.correct_option):
            correct += 1

    score = Score(quiz_id=quiz.id, user_id=current_user.id,
                  total_scored=correct, total_questions=len(quiz.questions))
    db.session.add(score)
    db.session.commit()
    return jsonify(score_to_dict(score)), 201


@user_bp.get("/scores")
@auth_required("token")
def my_scores():
    scores = Score.query.filter_by(user_id=current_user.id) \
        .order_by(Score.time_stamp_of_attempt.desc()).all()
    return jsonify([score_to_dict(s) for s in scores])
