# Day 6 – Authentication, roles and security

**Goal:** users register and log in; the admin pages are admin-only; users can book, view and cancel bookings.

**By the end, students can**
- explain sessions and cookies, and why passwords are hashed
- use Flask-Login: `login_user`, `logout_user`, `login_required`, `current_user`, `user_loader`
- write an `admin_required` decorator and check ownership (a user can only cancel *their own* booking)
- name the common security mistakes in MAD I projects and avoid them

BSCS2003 weeks covered: 9 (application security).

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap Day 5; show that anyone can open `/admin/` right now |
| 0:10 – 0:25 | Sessions, cookies, hashing; how Flask-Login works |
| 0:25 – 1:05 | Live code: `LoginManager`, register, login, logout, navbar by role |
| 1:05 – 1:20 | Live code: `decorators.py`, protect admin routes; demo 403 as a normal user |
| 1:20 – 1:50 | Hands-on: auth + role checks in students' projects |
| 1:50 – 2:00 | Security checklist, homework (user-side flows) |

The booking flow (`book`, `bookings`, `cancel`) and the admin `users` / `bookings` pages are included in the code as the **reference for today's homework**. Demo booking for 5 minutes if time allows.

---

## Concepts in plain words

- **Session cookie** – after login, Flask stores the user's id in a cookie *signed* with `SECRET_KEY`. The browser sends it with every request. Users can read it but cannot change it without breaking the signature.
- **Flask-Login** – `login_user(user)` writes the session; `user_loader` turns the id back into a `User` on each request; `current_user` is that user (or an anonymous user); `@login_required` redirects anonymous visitors to the login page.
- **Hashing** – `check_password_hash(stored_hash, typed_password)`. Even the admin cannot see passwords.
- **Authentication vs authorisation** – *who are you* (login) vs *what may you do* (roles, ownership).
- **Decorator** – a function that wraps a route. `@admin_required` runs before the route and returns 403 for non-admins.
- **Hiding a link is not security** – the navbar hides admin links from users, but the real check is `@admin_required` on every admin route. Type the URL to prove it.
- **Ownership check** – `if booking.user_id != current_user.id: abort(403)`. Without it, any user could cancel anyone's booking by changing the id in the URL.
- **Flagged users** – blocked at login, and `user_loader` returns `None` for them, so an already logged-in user is logged out on their next click.
- **Same error message** for "wrong email" and "wrong password" – do not tell attackers which emails exist.

## Security checklist for projects

- [ ] Passwords hashed (`generate_password_hash`), never stored or printed in plain text
- [ ] Every admin route has `@admin_required`; every user route has `@login_required` (or `@user_required`)
- [ ] Ownership checked whenever a URL contains an id that belongs to a user
- [ ] Registration can never create an admin (role set in code, not from the form)
- [ ] All data-changing actions are POST, not GET links
- [ ] All input validated on the server
- [ ] Queries use SQLAlchemy, never f-strings in raw SQL
- [ ] `SECRET_KEY` read from an environment variable in real deployments

---

## Live-coding script

| # | Do | Say / show |
|---|---|---|
| 1 | Open `/admin/` in a private window | "Anyone can delete our venues" |
| 2 | `LoginManager` in `app.py`, `user_loader`, `login_view = "auth.login"` | `UserMixin` was already on the model since Day 3 |
| 3 | `register()` with validation; role hard-coded to `"user"` | Show the hash in DB Browser after registering |
| 4 | `login()` and `logout()`; `home_for(user)` redirects by role | Wrong password → same message as unknown email |
| 5 | `base.html`: `current_user.is_authenticated`, `current_user.is_admin` | Navbar changes per role |
| 6 | `decorators.py`: `admin_required` using `@wraps` + `@login_required` + `abort(403)` | Decorator order matters: route on top, guard below |
| 7 | Add `@admin_required` to every admin route; add the 403 error page | Log in as Priya, type `/admin/` → 403 |
| 8 | Admin `users` page with Flag / Unflag (POST); flagged login refused | Flag Priya while she is logged in in another browser → she is logged out |
| 9 | (Homework reference) `book`, `bookings`, `cancel` with ownership check | Change the booking id in the cancel form via DevTools → 403 |

---

## Run & check

```bash
cd eventhub
source .venv/bin/activate
python app.py
python seed_demo.py     # if the database is empty
```

| Account | Email | Password |
|---|---|---|
| Admin | admin@eventhub.com | admin123 |
| User | priya@example.com | user123 |
| User | rahul@example.com | user123 |

- Logged out: `/admin/` → login page. As Priya: `/admin/` → 403; booking works; "My bookings" lists them; cancel frees the seats.
- As admin: Users page → flag Rahul → Rahul cannot log in.
- If you kept the Day 5 database, it still works: the tables did not change today.

## Common errors

| Error | Fix |
|---|---|
| `Exception: Missing user_loader or request_loader` | define `@login_manager.user_loader` and call `login_manager.init_app(app)` |
| `AttributeError: 'AnonymousUserMixin' object has no attribute 'is_admin'` | check `current_user.is_authenticated` before `is_admin` |
| Redirect loop on `/login` | the login route itself has `@login_required` – remove it |
| Logged out after every restart | `SECRET_KEY` changes each run (e.g. `os.urandom`) – use a fixed value |
| `check_password_hash` always False | the password was stored without hashing, or hashed twice |
| Decorator does nothing | it is **above** `@route`; it must be **below** it |
| `AssertionError: View function mapping is overwriting an existing endpoint` | decorator missing `@wraps(view)` |

## Homework

1. Build the user-side flows of your project (the main action a user takes, history, cancel/undo).
2. Go through the security checklist above for your project.
3. Try to break your own app: open admin URLs as a user, change ids in URLs, submit forms with DevTools edits.
