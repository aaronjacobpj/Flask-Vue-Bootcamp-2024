# MAD I Bootcamp – EventHub (10 days)

We build **one app from scratch, step by step**: **EventHub**, a multi-user event-booking app.
Each teaching day adds one layer. By Day 9 students have a complete MAD I project they fully understand.

- **7 teaching sessions** – Days 1, 2, 3, 5, 6, 8, 9 (live coding, about 2 hours each)
- **3 doubt-clearing sessions** – Days 4, 7, 10, each closing a build phase (no new topics)

Courses: BSCS2003P (MAD I project) · BSCS2003 (MAD I theory)

EventHub has the same shape as recent MAD I projects (an admin, users, a bookable resource, search, summaries, an API) but it is not a term's project statement, so students copy patterns, not code.

---

## 1. The app in one picture

```
 Browser (HTML + Bootstrap 5, a little JavaScript, Chart.js)     http://127.0.0.1:5000
        │  HTTP: GET pages, POST forms, JSON from /api
        ▼
 Flask app
   routes/user.py   routes/auth.py   routes/admin.py   api.py
        │   Jinja2 templates render the HTML on the server
        ▼
 Flask-SQLAlchemy  ──►  SQLite (instance/eventhub.db, created by code)
```

**Two roles**

| Role | How they get in | What they can do |
|---|---|---|
| Admin | Created automatically on first run – no sign-up | Create, edit, delete venues and events; view all bookings; search users, venues, events; flag users; summary charts |
| User | Registers with name, email and password | Browse and search events, book seats, cancel, booking history, personal summary charts |

---

## 2. Day-wise plan

| Day | Session | Topic | What gets built | Folder |
|---|---|---|---|---|
| 1 | Teaching 1 | How the web works + first Flask app | Flask app with routes, path variables, query strings | `day-01-web-basics-and-flask` |
| 2 | Teaching 2 | HTML, CSS, Bootstrap + Jinja2 | `base.html` layout, 4 pages with template inheritance | `day-02-templates-and-bootstrap` |
| 3 | Teaching 3 | Models: SQLite + Flask-SQLAlchemy | 4 models, app factory, database + admin created by code | `day-03-models-and-database` |
| 4 | Doubt clearing 1 | Setup, templates, schema review | – (notes only) | `day-04-doubt-clearing-1` |
| 5 | Teaching 4 | Controllers: CRUD, forms, search | Blueprints, admin CRUD with validation, search | `day-05-crud-and-search` |
| 6 | Teaching 5 | Authentication, roles, security | Register/login/logout, `@admin_required`, booking + cancel, flag users | `day-06-auth-and-security` |
| 7 | Doubt clearing 2 | Mid-project code review, debugging | – (notes only) | `day-07-doubt-clearing-2` |
| 8 | Teaching 6 | REST APIs, JavaScript, charts | Flask-RESTful API, Chart.js summaries, `fetch()` | `day-08-apis-and-charts` |
| 9 | Teaching 7 | Testing, deployment, report, video | pytest suite, pinned requirements, README, report + video templates | `day-09-testing-and-submission` |
| 10 | Doubt clearing 3 | Final clinic + mock viva | – (notes only) | `day-10-doubt-clearing-3` |

Every teaching-day folder contains:

- `NOTES.md` – the session plan: goal, timed agenda, concepts in plain words, a **live-coding script** (what to type, in what order, what to say), how to run and check, common errors, homework.
- `eventhub/` – the **complete code as it should look at the end of that day**. Teach live from the previous day's folder; if a demo breaks or runs long, copy in this folder and carry on. A student who missed a day copies it and continues.

Doubt-day folders contain `NOTES.md` only: format, common errors, review checklists.

`day-09-testing-and-submission/eventhub` is the finished project.

---

## 3. Requirements coverage

| Typical MAD I requirement | Where |
|---|---|
| Admin and user login, role-based access, admin pre-exists | Day 3 (seed), Day 6 (auth + decorators) |
| Database created by code, not by hand | Day 3 |
| Admin: create / edit / delete the main resources | Day 5 |
| Admin: search users and resources | Day 5 |
| Admin: block (flag) users | Day 6 |
| User: search, book, cancel, history | Day 5 (search), Day 6 (booking) |
| Summary charts for admin and user | Day 8 |
| API endpoints for CRUD | Day 8 |
| Server-side and browser validation | Days 2, 5, 6, 8 |
| Responsive UI with Bootstrap | Day 2 onward |
| Frameworks: Flask, Jinja2, SQLite, HTML/CSS/Bootstrap, minimal JS | All days |

Check this table against your term's project statement on Day 1.

---

## 4. One-time setup (students' laptops)

| Tool | Version | Check |
|---|---|---|
| Python | 3.10 or newer | `python --version` |
| Git + GitHub account | any | `git --version` |
| VS Code + Python extension | any | – |
| DB Browser for SQLite | any | for *viewing* data only |
| Postman, or curl | any | `curl --version` |

Windows: use `py` if `python` is not found; activate the venv with `.venv\Scripts\activate`.

---

## 5. Running any day's code

```bash
cd day-XX-.../eventhub
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed_demo.py              # Day 3 onward, optional demo data (run once)
python app.py                    # http://127.0.0.1:5000
```

| Account | Email | Password |
|---|---|---|
| Admin (created by the app) | admin@eventhub.com | admin123 |
| Demo user (after `seed_demo.py`) | priya@example.com | user123 |
| Demo user | rahul@example.com | user123 |

Day 9 only: `pytest -v` runs 19 tests. To start from an empty database, delete `instance/eventhub.db`.

---

## 6. Final folder structure

```
eventhub/
├── app.py              # create_app(): config, db, login manager, blueprints, error pages
├── config.py           # Config, TestConfig
├── models.py           # User, Venue, Event, Booking
├── seed.py             # creates the admin on startup
├── seed_demo.py        # optional demo data
├── decorators.py       # admin_required, user_required
├── api.py              # Flask-RESTful: venues and events
├── routes/
│   ├── auth.py         # register, login, logout
│   ├── admin.py        # dashboard, venue/event CRUD, users, bookings, search, summary
│   └── user.py         # browse + search, book, my bookings, cancel, summary
├── templates/
│   ├── base.html  index.html  error.html
│   ├── auth/   login  register
│   ├── admin/  dashboard  venue_form  event_form  users  bookings  search  summary
│   └── user/   book  bookings  summary
├── static/  css/style.css   js/app.js
├── tests/   conftest.py   test_app.py
├── requirements.txt   pytest.ini   README.md   .gitignore
```

---

## 7. Routes and API (final)

**Pages**

| URL | Who | Purpose |
|---|---|---|
| `/` (`?q=`) | anyone | Upcoming events, search |
| `/register`, `/login`, `/logout` | – | Authentication |
| `/events/<id>/book` | user | Book seats |
| `/bookings`, `/bookings/<id>/cancel` | user | History, cancel (POST) |
| `/summary` | user | Personal charts |
| `/admin/` | admin | Stats + venues with their events |
| `/admin/venues/new`, `/admin/venues/<id>/edit`, `/admin/venues/<id>/delete` | admin | Venue CRUD |
| `/admin/events/new`, `/admin/events/<id>/edit`, `/admin/events/<id>/delete` | admin | Event CRUD |
| `/admin/users`, `/admin/users/<id>/toggle-flag` | admin | Users, flag / unflag |
| `/admin/bookings` | admin | All bookings |
| `/admin/search?q=&type=` | admin | Search users, venues, events |
| `/admin/summary` | admin | Charts |

**API**

| Method | URL | Who | Purpose |
|---|---|---|---|
| GET / POST | `/api/venues` | GET: anyone, POST: admin | List / create |
| GET / PUT / DELETE | `/api/venues/<id>` | GET: anyone, others: admin | One venue (with events) / update / delete |
| GET / POST | `/api/events` (`?upcoming=1`) | GET: anyone, POST: admin | List / create |
| GET / PUT / DELETE | `/api/events/<id>` | GET: anyone, others: admin | One event (with `seats_left`) / update / delete |

---

## 8. Doubt-clearing sessions

| Day | Focus | Format |
|---|---|---|
| 4 | Setup, templates, database schema | 30 min common errors; 75 min schema reviews (about 5 min each); 15 min wrap-up |
| 7 | CRUD, auth, mid-project review | 20 min live debugging; 80 min screen-share code reviews; 20 min Q&A |
| 10 | Final clinic + mock viva | 45 min report and video; 60 min mock vivas (about 5 min each); 15 min submission checklist |

Students post doubts in a shared form by 12:00 noon on the day, with the repo link and the full error text. Details and checklists are in each day's `NOTES.md`.
