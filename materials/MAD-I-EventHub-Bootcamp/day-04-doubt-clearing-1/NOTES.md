# Day 4 – Doubt clearing 1: setup, templates and schema review

**Goal:** no student enters Day 5 with a broken setup or a schema that will need rewriting later.

No new topics today. There is no code folder: students continue from `day-03-models-and-database/eventhub` or their own project.

---

## Before the session

- Students submit doubts in the shared form **by 12:00 noon**, with: repo link, the error text (copy-paste, not a photo), what they tried.
- Students upload their ER diagram and a screenshot of their database tables.
- The mentor groups doubts by theme and picks the 3–4 most common for the first block.

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:30 | Common errors, solved live on screen (pick from the list below) |
| 0:30 – 1:45 | Schema reviews in breakout rooms, about 5 minutes per student, using the checklist |
| 1:45 – 2:00 | Wrap-up: patterns seen in reviews, what to finish before Day 5 |

---

## Common errors to cover

| Symptom | Cause | Fix |
|---|---|---|
| `ModuleNotFoundError` for flask / flask_sqlalchemy | venv not active, or packages installed globally | activate `.venv`, `pip install -r requirements.txt` |
| VS Code runs the wrong Python | interpreter not set | `Ctrl/Cmd+Shift+P` → "Python: Select Interpreter" → `.venv` |
| `TemplateNotFound` | wrong folder name or path | `templates/` next to `app.py`; sub-folders included in the name: `"auth/login.html"` |
| `BuildError` in `url_for` | function name typo, or a blueprint prefix missing (from Day 5: `"admin.dashboard"`) | use the function name |
| `Working outside of application context` | DB call at import time or in a shell | wrap in `with app.app_context():` |
| Model change not reflected | `create_all()` does not alter tables | delete `instance/*.db` and rerun |
| `IntegrityError: NOT NULL constraint failed` | a required column left empty | set it, or give it a `default=` |
| Circular import between `app.py` and `models.py` | `models.py` imports `app` | create `db = SQLAlchemy()` in `models.py`, call `db.init_app(app)` in `app.py` |
| Git pushes `.venv/` or the `.db` file | no `.gitignore` | add it, then `git rm -r --cached .venv instance` |

## Schema review checklist (5 minutes per student)

- [ ] Every role and feature in the project statement can be stored somewhere
- [ ] Every table has an integer primary key `id`
- [ ] Every one-to-many has the foreign key on the "many" side
- [ ] A many-to-many with extra data (dates, scores, quantities, status) is its own model
- [ ] Unique fields are marked `unique=True` (email, username)
- [ ] Passwords are stored as hashes
- [ ] Roles are a column (or a Role table), not separate user tables
- [ ] No column stores what can be calculated (totals, counts, "seats left")
- [ ] Dates use `db.Date` / `db.DateTime`, not strings
- [ ] `cascade` is set where deleting a parent should delete children
- [ ] The database and the admin are created by code on a fresh run

## Exit check (each student, before leaving)

1. Fresh clone → `pip install -r requirements.txt` → `python app.py` works.
2. Deleting the `.db` file and rerunning recreates all tables and the admin.
3. The ER diagram matches `models.py`.
