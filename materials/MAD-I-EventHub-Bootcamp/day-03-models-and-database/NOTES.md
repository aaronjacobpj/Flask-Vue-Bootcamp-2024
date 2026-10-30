# Day 3 – Models with SQLite + Flask-SQLAlchemy

**Goal:** EventHub stores its data in SQLite. Tables and the admin user are created by code on first run.

**By the end, students can**
- turn a project statement into entities, attributes and relationships (ER diagram)
- write Flask-SQLAlchemy models with primary keys, foreign keys and `db.relationship`
- create the database with `db.create_all()` and seed the admin, without touching DB Browser

BSCS2003 weeks covered: 4 (models: introduction to databases).

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap Day 2 |
| 0:10 – 0:35 | ER design on the whiteboard: find nouns (entities) and verbs (relationships) in the EventHub statement |
| 0:35 – 1:15 | Live code: `config.py`, `models.py`, `seed.py`, `create_app()`; run and open the DB |
| 1:15 – 1:50 | Hands-on: students draw their ER diagram and write `models.py` |
| 1:50 – 2:00 | Recap, homework (bring the ER diagram to Day 4) |

---

## Concepts in plain words

- **ORM** – write Python classes; SQLAlchemy writes the SQL. One class = one table, one attribute = one column, one object = one row.
- **Primary key / foreign key** – `id` identifies a row; `venue_id = db.ForeignKey("venue.id")` points an event at its venue.
- **One-to-many** – one venue has many events. Put the foreign key on the "many" side (`Event.venue_id`).
- **Many-to-many with data** – users and events meet through `Booking`, which also stores `seats` and `status`. When the link has its own data, make it a model.
- **`db.relationship`** – lets you write `venue.events` and `event.venue` instead of writing joins. `cascade="all, delete-orphan"` deletes children with the parent.
- **Calculated, not stored** – `seats_left` is a `@property` computed from bookings, so it can never disagree with them.
- **App factory** – `create_app()` builds the app. It makes testing easy on Day 9 (we pass a test config).
- **Created by code** – `db.create_all()` builds missing tables; `create_admin()` adds the admin if missing. Graders run your code on a fresh machine: a hand-made `.db` file will not be there.
- **Password hash** – `generate_password_hash` stores a salted hash, never the password.

## Database design (draw this first)

```
User ──< Booking >── Event >── Venue
```

| Table | Columns |
|---|---|
| User | id, name, email (unique), password_hash, role (`admin`/`user`), is_flagged, created_at |
| Venue | id, name, city, address, capacity |
| Event | id, venue_id → Venue, title, description, date_time, price, total_seats |
| Booking | id, user_id → User, event_id → Event, seats, booked_at, status (`booked`/`cancelled`) |

---

## Live-coding script

| # | Do | Say / show |
|---|---|---|
| 1 | `pip install flask-sqlalchemy flask-login`, update `requirements.txt` | Flask-Login is used on Day 6; installing now avoids a model change later |
| 2 | `config.py` with `SECRET_KEY`, `SQLALCHEMY_DATABASE_URI`, admin email/password | All settings in one place, overridable by environment variables |
| 3 | `models.py`: `db = SQLAlchemy()`, then `Venue`, `Event` | Start with the one-to-many pair |
| 4 | Add `User` and `Booking`, with `back_populates` on both sides | Draw the arrow for each relationship as you type it |
| 5 | Add `seats_booked`, `seats_left`, `is_upcoming` properties | Ask: "should seats_left be a column?" – discuss why not |
| 6 | `seed.py` → `create_admin(app)` | Admin is never registered through a form |
| 7 | Rewrite `app.py` as `create_app()` with `db.init_app` and `create_all()` in an app context | Explain "working outside of application context" before anyone hits it |
| 8 | Run it; open `instance/eventhub.db` in DB Browser | Show the 4 tables, the admin row, the hashed password |
| 9 | Run `python seed_demo.py`; reload `/` and `/admin` | Templates now use `event.venue.name` – relationships in action |
| 10 | Python shell: `with app.app_context(): Venue.query.first().events` | Query practice: `filter_by`, `filter`, `order_by`, `count` |

---

## Run & check

```bash
cd eventhub
source .venv/bin/activate
pip install -r requirements.txt
python app.py                # creates instance/eventhub.db + admin
python seed_demo.py          # optional demo data (run once, in another terminal)
```

- `/` lists upcoming events from the database; `/admin` groups events by venue with booked / total seats.
- Delete `instance/eventhub.db` and run again: everything is recreated.

## Common errors

| Error | Fix |
|---|---|
| `RuntimeError: Working outside of application context` | DB code must run inside `with app.app_context():` |
| Changed a model but the table did not change | `create_all()` never alters existing tables – delete `instance/eventhub.db` and run again |
| `sqlalchemy.exc.IntegrityError: UNIQUE constraint failed: user.email` | the email already exists – check before inserting |
| `NoForeignKeysError` / relationship errors | the `ForeignKey("venue.id")` string uses the **table** name (lower-case class name) |
| `AttributeError: 'dict' object has no attribute 'venue'` | templates still expect yesterday's dicts – use `event.venue.name` |

## Homework

1. Draw your project's ER diagram neatly (it goes in the report) and bring it to Day 4.
2. Write all models for your project and make the database create itself.
3. In a Python shell, add one row to each table and query it back.
