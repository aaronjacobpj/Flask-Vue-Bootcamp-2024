# Day 5 – Controllers: CRUD, forms and search

**Goal:** the admin can create, edit and delete venues and events through forms, and search everything.

**By the end, students can**
- split routes into blueprints
- handle GET and POST in one route, read `request.form`, validate on the server and `flash` messages
- use the Post/Redirect/Get pattern, delete with a POST form, and return 404 for missing rows
- search with `ilike`

BSCS2003 weeks covered: 5 (controllers: business logic).

> The admin pages are **open to everyone** at the end of today. Day 6 adds login and `@admin_required`. Say this out loud so nobody submits it like this.

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap: Model (Day 3) + View (Day 2); today is the Controller |
| 0:10 – 0:25 | Blueprints: move routes into `routes/user.py`, `routes/auth.py`, `routes/admin.py` |
| 0:25 – 1:15 | Live code: venue create + edit (one function), delete, then events with validation; flash messages |
| 1:15 – 1:25 | Live code: search for users (events) and admin (users / venues / events) |
| 1:25 – 1:50 | Hands-on: CRUD for the main entity of each student's project |
| 1:50 – 2:00 | Recap, homework |

---

## Concepts in plain words

- **Blueprint** – a group of routes in its own file. `Blueprint("admin", __name__, url_prefix="/admin")` → every route starts with `/admin`, and `url_for` names become `"admin.dashboard"`.
- **GET vs POST** – GET shows the form; POST submits it. `methods=["GET", "POST"]` on the route, `if request.method == "POST":` inside.
- **`request.form.get("capacity", type=int)`** – returns `None` instead of crashing when the value is not a number.
- **Server-side validation** – HTML `required` and `min` are a convenience. Anyone can bypass them, so check everything again in Python.
- **`flash()`** – stores a one-time message shown on the next page (`base.html` displays them).
- **Post/Redirect/Get** – after a successful POST, `redirect(...)`. Otherwise pressing refresh submits the form again.
- **Delete with POST** – a plain link can be triggered by a crawler or a prefetch. Deleting data is always a POST form (with a `confirm()` prompt).
- **`db.get_or_404(Venue, venue_id)`** – returns the row or a 404 page. No `None` checks needed.
- **One function for new + edit** – `venue_form(Venue())` for new, `venue_form(existing)` for edit. Same template, same validation.
- **`ilike`** – case-insensitive search: `Event.title.ilike(f"%{q}%")`. SQLAlchemy escapes `q`, so it is safe from SQL injection.

---

## Live-coding script

| # | Do | Say / show |
|---|---|---|
| 1 | Create `routes/` with `user.py`, `auth.py`, `admin.py`; register blueprints in `create_app` | Show the `url_for` errors, then fix names to `"user.index"`, `"admin.dashboard"` |
| 2 | Add flash display to `base.html` | Bootstrap alert classes match our categories: `success`, `danger`, `info`, `warning` |
| 3 | `new_venue` + `venue_form()` – GET first, then POST that saves without validation | Submit an empty form – see the crash or the bad row |
| 4 | Add validation + `flash` errors; keep typed values with `request.form.get(..., venue.name)` | The form remembers input when validation fails |
| 5 | Add `edit_venue` reusing `venue_form()` | Same template – `venue.id is not none` decides the heading |
| 6 | Add `delete_venue` (POST) and the form button with `confirm()` | Cascade: the venue's events disappear too |
| 7 | Events: `event_form()` with a venue `<select>`, `datetime-local`, seats ≤ capacity | `datetime.fromisoformat` parses the `datetime-local` value |
| 8 | Edit rule: seats cannot go below seats already booked | Business rules live in the controller |
| 9 | User search on `/` with `?q=` across title, venue name, city | `join(Venue)` lets us filter on the venue's columns |
| 10 | Admin `/admin/search` with a type selector | One template, three result shapes |

---

## Run & check

```bash
cd eventhub
source .venv/bin/activate
python app.py
python seed_demo.py     # if the database is empty
```

- `/admin/` → add, edit, delete a venue; add an event from a venue card (venue pre-selected).
- Try invalid input: empty name, capacity `0`, seats above capacity. Each shows a red message and keeps what you typed.
- `/?q=chennai` filters events; `/admin/search?q=pr&type=users` finds Priya.
- `/admin/venues/999/edit` → 404 page.

## Common errors

| Error | Fix |
|---|---|
| `BuildError: Could not build url for endpoint 'index'` | with blueprints the name is `"user.index"` |
| `405 Method Not Allowed` | route is missing `methods=["GET", "POST"]`, or the delete form uses GET |
| Form submits but nothing saves | missing `db.session.commit()`, or `db.session.add()` for a new object |
| `TypeError: '<' not supported between 'NoneType' and 'int'` | `request.form.get(..., type=int)` returned `None` – check for `None` first |
| `ValueError: Invalid isoformat string` | empty or wrong date – catch `ValueError` and flash a message |
| Refresh shows "Confirm form resubmission" | return `redirect(...)` after a successful POST |
| Flash messages never appear | `SECRET_KEY` not set, or `base.html` does not render `get_flashed_messages` |

## Homework

1. Finish create / edit / delete for **every** entity in your project.
2. Add the search your project statement asks for.
3. Test every form with empty, negative and very long input.
