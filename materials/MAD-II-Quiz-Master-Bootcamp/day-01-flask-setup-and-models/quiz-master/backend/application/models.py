from datetime import datetime, date

from flask_security import UserMixin, RoleMixin

from .extensions import db

# Many-to-many: users <-> roles
class RolesUsers(db.Model):
    __tablename__ = "roles_users"
    id = db.Column(db.Integer(), primary_key=True)
    user_id = db.Column(db.Integer(), db.ForeignKey("user.id"))
    role_id = db.Column(db.Integer(), db.ForeignKey("role.id"))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True, nullable=False)
    description = db.Column(db.String(255))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)  # username
    password = db.Column(db.String(255), nullable=False)
    # Additional user fields
    full_name = db.Column(db.String(120), nullable=False)
    qualification = db.Column(db.String(120))
    dob = db.Column(db.Date)
    active = db.Column(db.Boolean, default=True)
    # Flask-Security-Too fields
    # Required by Flask-Security-Too: changing it invalidates all tokens
    fs_uniquifier = db.Column(db.String(64), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_visit = db.Column(db.DateTime, default=datetime.utcnow)

    roles = db.relationship("Role", secondary="roles_users", backref=db.backref("users", lazy="dynamic"))
    scores = db.relationship("Score", backref="user", cascade="all, delete-orphan")


class Subject(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True, nullable=False)
    description = db.Column(db.Text)
    chapters = db.relationship("Chapter", backref="subject", cascade="all, delete-orphan")


class Chapter(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject_id = db.Column(db.Integer, db.ForeignKey("subject.id"), nullable=False)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    quizzes = db.relationship("Quiz", backref="chapter", cascade="all, delete-orphan")


class Quiz(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chapter_id = db.Column(db.Integer, db.ForeignKey("chapter.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    date_of_quiz = db.Column(db.Date, default=date.today)
    time_duration = db.Column(db.Integer, default=10)  # minutes
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    questions = db.relationship("Question", backref="quiz", cascade="all, delete-orphan")
    scores = db.relationship("Score", backref="quiz", cascade="all, delete-orphan")


class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    statement = db.Column(db.Text, nullable=False)
    option1 = db.Column(db.String(255), nullable=False)
    option2 = db.Column(db.String(255), nullable=False)
    option3 = db.Column(db.String(255))
    option4 = db.Column(db.String(255))
    correct_option = db.Column(db.Integer, nullable=False)  # 1..4


class Score(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quiz_id = db.Column(db.Integer, db.ForeignKey("quiz.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    time_stamp_of_attempt = db.Column(db.DateTime, default=datetime.utcnow)
    total_scored = db.Column(db.Integer, default=0)
    total_questions = db.Column(db.Integer, default=0)
