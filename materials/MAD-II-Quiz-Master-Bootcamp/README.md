# MAD II Bootcamp – Quiz Master (10 days)

We build **one app from scratch, step by step**: **Quiz Master**, a multi-user exam-preparation app.
Each day adds one layer. By Day 7 students have a complete MAD II project they fully understand.

- **Days 1–7** – teaching sessions (live coding, ~2 hours each)
- **Days 8–10** – doubt-clearing sessions (no new topics)

---

## 1. The app in one picture

```
 Browser (Vue 3 Options API + Router + Vuex + Bootstrap) http://localhost:5173
        │  JSON over HTTP + header "Authentication-Token"
        ▼
 Flask REST API (Flask-Security-Too, SQLAlchemy)         http://localhost:5000/api
        │                     │                   │
        ▼                     ▼                   ▼
   SQLite database      Redis (cache)      Redis (Celery queue) ──► Celery worker + beat
                                                                    (CSV export, reminders,
                                                                     monthly report → email)
```

**Two roles**

| Role  | How they get in                       | What they can do |
|-------|---------------------------------------|------------------|
| Admin (Quiz Master) | Created automatically on first run – no sign-up | Manage subjects → chapters → quizzes → questions, search, block users, see summary charts, export CSV, run jobs |
| User  | Registers with email + password       | Attempt quizzes (timer), see scores and summary charts, export own scores as CSV |

---

## 2. Day-wise plan

| Day | Topic | What gets built | Folder |
|-----|-------|-----------------|--------|
| 1 | Project setup & database | Flask app factory, SQLAlchemy models, admin seeded | `day-01-flask-setup-and-models` |
| 2 | Token-based authentication | Register / login / logout APIs, roles (RBAC), CORS | `day-02-token-auth` |
| 3 | REST APIs | CRUD for subjects, chapters, quizzes, questions; attempt & score a quiz; search | `day-03-rest-apis` |
| 4 | Vue 3 + Router + Vuex basics | Vite project, login/register pages, Vuex auth store, route guards | `day-04-vue-router-vuex` |
| 5 | Full frontend | Admin screens (CRUD, users, search) and user screens (quiz with timer, scores) | `day-05-admin-and-user-ui` |
| 6 | Celery + Redis background jobs | Async CSV export, daily reminder, monthly HTML report (email) | `day-06-celery-redis-jobs` |
| 7 | Caching, charts, final review | Redis caching with expiry, ApexCharts summaries (vue3-apexcharts), security & viva checklist | `day-07-caching-charts-final` |
| 8 | Doubt clearing 1 | Backend & auth doubts, debugging students' projects | – |
| 9 | Doubt clearing 2 | Vue / Vuex doubts, UI issues | – |
| 10 | Doubt clearing 3 | Celery / Redis / caching doubts, project report & viva rehearsal | – |

Every day folder contains:

- `NOTES.md` – the session plan: goal, timed agenda, concepts in plain words, build steps, how to test, common errors, homework.
- `quiz-master/` – the **complete code as it should look at the end of that day**. A student who missed a day copies this folder and continues.

`day-07-caching-charts-final/quiz-master` is the finished project.

---

## 3. Requirements coverage

**Core**

| Requirement | Where |
|---|---|
| Admin & user login, role-based access, admin pre-exists | Day 1 (seed), Day 2 (auth APIs), Day 4 (route guards) |
| Admin: create/edit/delete subjects, chapters, quizzes (date, duration), MCQ questions | Day 3 (APIs), Day 5 (screens) |
| Admin: search users / subjects / quizzes | Day 3 (`/api/admin/search`), Day 5 (navbar search) |
| User: attempt quiz with timer, auto-submit, scores recorded | Day 3 (scoring on server), Day 5 (quiz page) |
| User: view past scores | Day 3, Day 5 |
| Summary charts (admin & user) | Day 7 |
| Scheduled job – daily reminders | Day 6 |
| Scheduled job – monthly activity report (HTML email) | Day 6 |
| User-triggered async job – export as CSV (user & admin) | Day 6 |
| Caching with expiry, API performance | Day 7 |
| Frameworks: Flask, SQLite, VueJS, Bootstrap, Redis, Celery | All days |

**Optional / recommended**

| Feature | Where |
|---|---|
| Proper login framework (Flask-Security-Too, token based) | Day 2 |
| ApexCharts charts | Day 7 |
| Responsive UI for mobile & desktop (Bootstrap grid, collapsible navbar, scrollable tables) | Days 5 & 7 |
| Frontend validation (HTML5 `required`, `type=email`, `min`, `minlength`) + backend validation | Days 2, 3, 4, 5 |
| Styling with Bootstrap only (installed with npm, no custom CSS) | Days 4–5 |
| Admin can block / unblock users | Day 5 |
| PDF version of the monthly report | Described as an extension in Day 7 notes |

---

## 4. One-time setup (students' laptops)

| Tool | Version | Check |
|---|---|---|
| Python | 3.10 or newer | `python --version` |
| Node.js | 18 or newer (includes npm) | `node --version` |
| Redis | 6 or newer | `redis-cli ping` → `PONG` |
| MailHog (optional, Day 6) | any | open <http://localhost:8025> |
| VS Code + Postman/Thunder Client | any | – |

- **macOS:** `brew install redis mailhog` then `brew services start redis`
- **Ubuntu / WSL:** `sudo apt install redis-server` then `sudo service redis-server start`
- **Windows:** use **WSL (Ubuntu)** for Redis and Celery. Celery does not run properly on native Windows.

---

## 5. Running the final app (Day 7 code)

Open **5 terminals**:

```bash
# 1. Redis (skip if it already runs as a service)
redis-server

# 2. Backend API
cd quiz-master/backend
python -m venv .venv && source .venv/bin/activate   # Windows (WSL) same
pip install -r requirements.txt
python seed_demo.py        # optional demo data (run once)
python app.py              # http://localhost:5000

# 3. Celery worker (same venv, backend folder)
celery -A worker.celery worker --loglevel=info

# 4. Celery beat – the scheduler (same venv, backend folder)
celery -A worker.celery beat --loglevel=info

# 5. Frontend
cd quiz-master/frontend
npm install
npm run dev                # http://localhost:5173
```

Logins: admin `admin@quizmaster.com` / `admin123`, demo user `user@quizmaster.com` / `user123` (after `seed_demo.py`).
Emails: start `mailhog` and open <http://localhost:8025>. Without MailHog, emails are printed in the Celery worker terminal.

---

## 6. Final folder structure

```
quiz-master/
├── backend/
│   ├── app.py                 # create_app(): config, extensions, blueprints
│   ├── config.py              # all settings in one place
│   ├── worker.py              # Celery entry point
│   ├── seed_demo.py           # optional demo data
│   ├── requirements.txt
│   ├── templates/monthly_report.html
│   └── application/
│       ├── extensions.py      # db, security, cache objects
│       ├── models.py          # User, Role, Subject, Chapter, Quiz, Question, Score
│       ├── seed.py            # tables + roles + admin
│       ├── serializers.py     # model -> dict
│       ├── utils.py           # small helpers (errors, json input, dates)
│       ├── celery_app.py      # Celery + Flask + beat schedule
│       ├── tasks.py           # the 3 background jobs
│       ├── mailer.py          # send email
│       └── api/
│           ├── auth.py        # register, login, logout, me
│           ├── resources.py   # subjects / chapters / quizzes / questions CRUD (+ cache)
│           ├── user.py        # attempt, submit, my scores
│           ├── admin.py       # users, block, all scores, search
│           ├── jobs.py        # export CSV + run jobs
│           └── summary.py     # chart data (+ cache)
└── frontend/
    ├── package.json  vite.config.js  index.html
    └── src/
        ├── main.js  App.vue  api.js
        ├── router/index.js
        ├── store/index.js     # Vuex: logged-in user + message only
        ├── components/ NavBar  FlashMessage  ExportButton  BarChart
        └── views/
            ├── LoginView  RegisterView  NotFound
            ├── admin/ AdminDashboard  ChapterQuizzes  QuizQuestions  UsersView  SearchView  AdminSummary
            └── user/  UserDashboard  QuizAttempt  ScoresView  UserSummary
```

---

## 7. API reference (final)

| Method | URL | Who | Purpose |
|---|---|---|---|
| POST | `/api/register` | public | Create user account |
| POST | `/api/login` | public | Returns `token` + `user` |
| POST | `/api/logout` | logged in | Invalidates all tokens of the user |
| GET | `/api/me` | logged in | Current user |
| GET / POST | `/api/subjects` | GET: all, POST: admin | List (with chapters) / create |
| PUT / DELETE | `/api/subjects/<id>` | admin | Edit / delete (cascades) |
| GET / POST | `/api/subjects/<id>/chapters` | GET: all, POST: admin | List / create chapters |
| PUT / DELETE | `/api/chapters/<id>` | admin | Edit / delete chapter |
| GET | `/api/quizzes` | logged in | All quizzes (users only see quizzes that have questions) |
| GET / POST | `/api/chapters/<id>/quizzes` | GET: all, POST: admin | List / create quizzes |
| PUT / DELETE | `/api/quizzes/<id>` | admin | Edit / delete quiz |
| GET / POST | `/api/quizzes/<id>/questions` | admin | List (with answers) / create question |
| PUT / DELETE | `/api/questions/<id>` | admin | Edit / delete question |
| GET | `/api/quizzes/<id>/attempt` | user | Questions **without** answers |
| POST | `/api/quizzes/<id>/submit` | user | Server calculates and saves score |
| GET | `/api/scores` | logged in | My scores |
| GET | `/api/admin/users` | admin | All users |
| PATCH | `/api/admin/users/<id>/toggle` | admin | Block / unblock |
| GET | `/api/admin/scores` | admin | All attempts |
| GET | `/api/admin/search?q=` | admin | Search users, subjects, quizzes |
| POST | `/api/export` | logged in | Start CSV export job → `task_id` |
| GET | `/api/export/<task_id>` | logged in | Job state |
| GET | `/api/export/<task_id>/file` | owner | Download CSV |
| POST | `/api/admin/jobs/reminders` · `/monthly-report` | admin | Run a scheduled job now |
| GET | `/api/admin/summary` · `/api/summary` | admin · user | Chart data (cached 60 s) |

---

## 8. Doubt-clearing sessions (Days 8–10)

Each session is about 2 hours. Students send their doubts the day before (Google Form / group), so the mentor can group similar ones.

**Day 8 – Backend & auth**
- 30 min: go over the most common doubts from the form
- 60 min: live debugging of student projects (screen share): 401/403 errors, `fs_uniquifier` missing, SQLAlchemy relationship errors, CORS errors
- 30 min: Q&A, plus a 5-minute model-design review per volunteer

**Day 9 – Frontend**
- Options API issues (`this` inside arrow functions vs normal functions, a value not declared in `data()` not updating the screen), Vuex flow (component → dispatch action → commit mutation → state), route guards and redirect loops, axios interceptor, token not sent
- Bootstrap layout fixes for mobile
- Live: one student builds a small CRUD screen with mentor guidance

**Day 10 – Jobs, caching & submission**
- Celery worker not picking up tasks, beat not firing, Redis not running, Windows/WSL issues, stale cache after updates
- Project report structure (problem statement, ER diagram, API list, technologies, demo video)
- Viva rehearsal with the question bank in `day-07-caching-charts-final/NOTES.md`
