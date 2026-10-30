# Day 1 – Project setup & database models

**Goal:** a running Flask backend with all database tables and one admin user, created automatically.

**By the end, students can**
- explain what MAD II adds over MAD I (Flask serves only JSON, Vue builds the UI)
- structure a Flask project with an *app factory*
- design the Quiz Master database and write it with SQLAlchemy

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:15 | Bootcamp overview, show the finished app (Day 7 code), the 10-day plan |
| 0:15 – 0:30 | Architecture: API backend + SPA frontend, why two servers |
| 0:30 – 0:45 | Setup: Python venv, folders, `requirements.txt` |
| 0:45 – 1:25 | Live code: `config.py`, `extensions.py`, `models.py` (ER diagram on the board first) |
| 1:25 – 1:45 | Live code: `seed.py`, `app.py`, run and check the DB |
| 1:45 – 2:00 | Recap, Q&A, homework |

---

## Concepts in plain words

- **MAD I vs MAD II** – In MAD I Flask returned HTML pages (Jinja). In MAD II Flask returns **JSON only** (an API) and **Vue** draws the pages in the browser.
- **App factory** – instead of creating `app` at the top of a file, we write `create_app()`. It keeps setup in one place, avoids circular imports and makes testing easy.
- **extensions.py** – we create `db = SQLAlchemy()` *without* an app, and connect it later with `db.init_app(app)`. Any file can now `from .extensions import db`.
- **Flask-Security-Too** – a library that gives us password hashing, roles and tokens. Today we only use its user/role *models*; tokens come on Day 2.

## Database design (draw this first)

```
User ──< roles_users >── Role            (many-to-many: admin / user)
User ──< Score >── Quiz                  (a user's attempts)
Subject ──< Chapter ──< Quiz ──< Question
```

| Table | Important columns |
|---|---|
| User | email (username), password (hashed), full_name, qualification, dob, active, **fs_uniquifier**, last_visit |
| Role | name (`admin` / `user`) |
| Subject | name, description |
| Chapter | subject_id, name, description |
| Quiz | chapter_id, title, date_of_quiz, time_duration (minutes), remarks, created_at |
| Question | quiz_id, statement, option1..option4, correct_option (1–4) |
| Score | quiz_id, user_id, time_stamp_of_attempt, total_scored, total_questions |

`cascade="all, delete-orphan"` means: delete a subject → its chapters, quizzes and questions are deleted too.

`fs_uniquifier` is required by Flask-Security-Too. Each token contains it, so changing it logs the user out everywhere (we use this on Day 2).

---

## Build steps

| # | File | What & why |
|---|---|---|
| 1 | `backend/requirements.txt` | Flask, Flask-SQLAlchemy, Flask-Security-Too, bcrypt, email-validator |
| 2 | `backend/config.py` | One `Config` class: secret key, SQLite path, password salt, admin email/password |
| 3 | `backend/application/extensions.py` | `db` and `security` objects (no app yet) |
| 4 | `backend/application/models.py` | All 7 tables. `User` uses `UserMixin`, `Role` uses `RoleMixin` |
| 5 | `backend/application/seed.py` | `db.create_all()`, create roles `admin` + `user`, create the admin if missing |
| 6 | `backend/app.py` | `create_app()`: load config → `db.init_app` → `SQLAlchemyUserDatastore` → `security.init_app` → seed → `/api/health` |

Key idea in `seed.py` – the admin is **never registered**, it is created by code:

```python
datastore.create_user(email=..., password=hash_password(...), full_name="Quiz Master", roles=["admin"])
```

---

## Run & check

```bash
cd quiz-master/backend
python -m venv .venv
source .venv/bin/activate          # Windows CMD: .venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

- Open <http://localhost:5000/api/health> → `{"status": "ok"}`
- A file `backend/instance/quiz_master.db` is created. Open it with *DB Browser for SQLite* (or the VS Code SQLite extension) and show the tables, the admin row and the hashed password.

## Common errors

| Error | Fix |
|---|---|
| `ModuleNotFoundError: flask_security` | venv not activated, or `pip install` not run |
| `ValueError: ... fs_uniquifier` | the `User` model is missing `fs_uniquifier` |
| Changed a model but the table did not change | `create_all()` never alters existing tables – delete `instance/quiz_master.db` and run again |
| `RuntimeError: Working outside of application context` | DB code must run inside `with app.app_context():` |

## Homework

1. Draw the ER diagram neatly; it goes in the project report.
2. Open a Python shell and add a subject manually:
   `from app import app; from application.models import *` → `with app.app_context(): ...`
3. Read the Flask-Security-Too "Quick start – SQLAlchemy" page.
