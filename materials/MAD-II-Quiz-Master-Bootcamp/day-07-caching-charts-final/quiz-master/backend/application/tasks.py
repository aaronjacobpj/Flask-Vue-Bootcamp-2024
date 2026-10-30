"""Background jobs (run by the Celery worker, NOT by Flask).

1. export_csv        - user-triggered async job  (button click -> CSV file)
2. daily_reminders   - scheduled job (celery beat, every evening)
3. monthly_reports   - scheduled job (celery beat, 1st of every month)
"""
import csv
import os
from datetime import datetime, timedelta

from celery import shared_task
from flask import current_app, render_template
from sqlalchemy import func

from .extensions import db
from .mailer import send_email
from .models import User, Role, Quiz, Score


# --------------------------------------------------------------------------- 1
@shared_task
def export_csv(user_id, is_admin):
    """Admin -> one row per user with stats.  User -> one row per quiz attempt.
    Returns the file name; the API uses it to send the file for download."""
    os.makedirs(current_app.config["EXPORT_DIR"], exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S")

    if is_admin:
        filename = f"admin_users_{stamp}.csv"
        header = ["user_id", "full_name", "email", "quizzes_taken", "average_score_%", "status"]
        rows = []
        for u in User.query.filter(User.roles.any(Role.name == "user")).all():
            pct = [100 * s.total_scored / s.total_questions for s in u.scores if s.total_questions]
            rows.append([u.id, u.full_name, u.email, len(u.scores),
                         round(sum(pct) / len(pct), 1) if pct else 0,
                         "active" if u.active else "blocked"])
    else:
        filename = f"user{user_id}_scores_{stamp}.csv"
        header = ["quiz_id", "quiz_title", "chapter_id", "chapter", "date_of_quiz",
                  "attempted_at", "score", "total_questions", "remarks"]
        rows = [[s.quiz_id, s.quiz.title, s.quiz.chapter_id, s.quiz.chapter.name,
                 s.quiz.date_of_quiz, s.time_stamp_of_attempt.strftime("%Y-%m-%d %H:%M"),
                 s.total_scored, s.total_questions, s.quiz.remarks or ""]
                for s in Score.query.filter_by(user_id=user_id).all()]

    with open(os.path.join(current_app.config["EXPORT_DIR"], filename), "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(header)
        writer.writerows(rows)
    return filename


# --------------------------------------------------------------------------- 2
@shared_task
def daily_reminders():
    """Remind users who have not logged in for a day, or tell them about
    quizzes created in the last 24 hours."""
    since = datetime.utcnow() - timedelta(days=1)
    new_quizzes = Quiz.query.filter(Quiz.created_at >= since).all()
    sent = 0

    for user in User.query.filter(User.roles.any(Role.name == "user"), User.active.is_(True)).all():
        inactive = user.last_visit is None or user.last_visit < since
        if not (inactive or new_quizzes):
            continue
        quiz_list = "".join(f"<li>{q.title} ({q.chapter.subject.name})</li>" for q in new_quizzes)
        html = (f"<p>Hi {user.full_name},</p>"
                + (f"<p>New quizzes are waiting for you:</p><ul>{quiz_list}</ul>" if new_quizzes
                   else "<p>We missed you today! Log in and attempt a quiz.</p>")
                + "<p>- Quiz Master</p>")
        send_email(user.email, "Quiz Master - daily reminder", html)
        sent += 1
    return f"reminders sent: {sent}"


# --------------------------------------------------------------------------- 3
@shared_task
def monthly_reports(current_month=False):
    """HTML activity report of the PREVIOUS month for every user.
    current_month=True is used by the admin "run now" button so a demo shows data."""
    first_this_month = datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    if current_month:
        start, end = first_this_month, datetime.utcnow()
    else:
        start, end = (first_this_month - timedelta(days=1)).replace(day=1), first_this_month
    month_name = start.strftime("%B %Y")

    in_month = (Score.time_stamp_of_attempt >= start) & (Score.time_stamp_of_attempt < end)

    # Ranking: average % of every user who attempted something last month
    avg_pct = func.avg(100.0 * Score.total_scored / Score.total_questions)
    ranking = db.session.query(Score.user_id, avg_pct).filter(in_month) \
        .group_by(Score.user_id).order_by(avg_pct.desc()).all()
    rank_of = {uid: i + 1 for i, (uid, _) in enumerate(ranking)}

    sent = 0
    for user in User.query.filter(User.roles.any(Role.name == "user")).all():
        scores = Score.query.filter(in_month, Score.user_id == user.id).all()
        pct = [100 * s.total_scored / s.total_questions for s in scores if s.total_questions]
        html = render_template(
            "monthly_report.html", user=user, month=month_name, scores=scores,
            average=round(sum(pct) / len(pct), 1) if pct else 0,
            rank=rank_of.get(user.id), total_users=len(ranking),
        )
        send_email(user.email, f"Your Quiz Master report - {month_name}", html)
        sent += 1
    return f"reports sent: {sent}"
