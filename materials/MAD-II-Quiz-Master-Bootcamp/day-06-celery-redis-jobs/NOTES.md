# Day 6 – Background jobs with Celery & Redis

**Goal:** the three required backend jobs work: async CSV export, daily reminder, monthly activity report.

**By the end, students can**
- explain why slow work must not run inside a Flask request
- run a Celery worker and Celery beat with Redis as the broker
- write tasks that use the database and templates (Flask app context)
- start a job from Vue and download the result when it is ready

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:15 | Why background jobs? Draw the diagram below |
| 0:15 – 0:25 | Install/start Redis (and MailHog), `redis-cli ping` |
| 0:25 – 0:45 | Live code: config, `celery_app.py`, `worker.py`, start the worker |
| 0:45 – 1:05 | Task 1: `export_csv` + `api/jobs.py` + `ExportButton.vue` |
| 1:05 – 1:30 | Task 2 & 3: `daily_reminders`, `monthly_reports`, `mailer.py`, HTML template |
| 1:30 – 1:45 | Celery beat: schedules with `crontab`; admin "run now" buttons |
| 1:45 – 2:00 | Demo in MailHog, homework |

---

## Concepts in plain words

```
Vue ──POST /api/export──► Flask ──puts task──► Redis (queue) ──► Celery worker runs it
 ▲                          │ returns task_id at once                   │ writes CSV
 └── polls GET /api/export/<task_id> until SUCCESS, then downloads ◄────┘

Celery beat = an alarm clock. At 6 PM every day it puts "daily_reminders" in the queue;
on the 1st of every month it puts "monthly_reports".
```

- **Why?** Building a CSV or sending 500 emails can take seconds or minutes. The user should get a reply immediately, not wait (or time out).
- **Redis** – a very fast in-memory store. Celery uses it as the **broker** (queue of tasks) and **result backend** (status + return value of each task).
- **Worker** – a separate process that runs tasks. **Beat** – a separate process that schedules periodic tasks. Both must be running.
- **App context** – tasks run outside Flask requests. `FlaskTask` in `celery_app.py` wraps every task in `with app.app_context():` so `db`, models and `render_template` work.
- **MailHog** – a fake email server for development. Every mail sent to `localhost:1025` appears at <http://localhost:8025>. If MailHog is not running, our `send_email` prints the mail in the worker terminal instead – the demo still works.

---

## The three jobs (`application/tasks.py`)

| Job | Type | Trigger | What it does |
|---|---|---|---|
| `export_csv(user_id, is_admin)` | user-triggered, async | "Export as CSV" button | User: own attempts (quiz_id, title, chapter_id, chapter, date_of_quiz, attempted_at, score, total, remarks). Admin: one row per user (quizzes taken, average %, status). Returns the file name |
| `daily_reminders()` | scheduled | every day 18:00 (Asia/Kolkata) | Email users who have not logged in for 24 h, or list quizzes created in the last 24 h |
| `monthly_reports()` | scheduled | 1st of month 08:00 | HTML email per user: quizzes attempted, average %, rank among all users, table of attempts |

Security in the download API: a user may only download files that start with `user<their id>_`; admin files start with `admin_`.

---

## Build steps

| # | File | What & why |
|---|---|---|
| 1 | `requirements.txt` | add `celery`, `redis` |
| 2 | `config.py` | `CELERY` dict (broker, result backend, timezone), `EXPORT_DIR`, mail settings |
| 3 | `application/models.py` | `Quiz.created_at` (already present since Day 1 – used by reminders) |
| 4 | `application/celery_app.py` | `celery_init_app(app)`: FlaskTask, `beat_schedule` with `crontab` |
| 5 | `app.py` | call `celery_init_app(app)`, register `jobs_bp` |
| 6 | `worker.py` | `celery = app.extensions["celery"]` – what the `celery` command loads |
| 7 | `application/mailer.py` | `send_email(to, subject, html)` with `smtplib` |
| 8 | `application/tasks.py` + `templates/monthly_report.html` | the three `@shared_task`s |
| 9 | `application/api/jobs.py` | `POST /export`, `GET /export/<id>`, `GET /export/<id>/file`, `POST /admin/jobs/<name>` |
| 10 | `frontend/src/components/ExportButton.vue` | start → poll every second → download blob |
| 11 | `ScoresView.vue`, `UsersView.vue` | add `<ExportButton/>`; admin also gets "Send reminders now" / "Send monthly report now" |

---

## Run & check (5 terminals)

```bash
redis-server                                          # 1
mailhog                                               # 2 (optional) → http://localhost:8025
python app.py                                         # 3 (backend folder, venv active)
celery -A worker.celery worker --loglevel=info        # 4 (backend folder, venv active)
celery -A worker.celery beat --loglevel=info          # 5 (backend folder, venv active)
npm run dev                                           # frontend folder
```

1. User → My Scores → **Export as CSV** → button shows "Preparing CSV…" → file downloads. Watch the task in the worker terminal.
2. Admin → Users → **Export as CSV** → user statistics file.
3. Admin → **Send reminders now** / **Send monthly report now** → open MailHog.
4. Beat demo: in `celery_app.py` change the reminder schedule to `60.0`, restart beat, wait one minute.

Windows students: run Redis and Celery inside WSL. If you must run the worker on Windows, add `--pool=solo`.

## Common errors

| Error | Fix |
|---|---|
| Export stays "Preparing…" then fails | the worker is not running, or was started before the code change – restart it |
| `Connection refused 6379` | Redis not running (`redis-cli ping`) |
| `Received unregistered task` | start the worker with `-A worker.celery` from the **backend** folder |
| Scheduled task never runs | beat not started, or wrong timezone – check `timezone` in config |
| Changed `tasks.py` but nothing changed | Celery does not auto-reload – restart worker (and beat) |

## Homework

1. Send the daily reminder to a Google Chat space using an incoming webhook (`requests.post(url, json={"text": ...})`) as an alternative to email.
2. Add the quiz-wise ranking (top 3 users) to the monthly report.
