# Day 2 – Token-based authentication & roles

**Goal:** users can register and log in through JSON APIs, receive a token, and every protected API checks the token and the role.

**By the end, students can**
- explain session (cookie) login vs token login
- protect routes with `@auth_required("token")` and `@roles_required("admin")`
- explain CORS and why the browser needs it in our setup

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap Day 1, run the app |
| 0:10 – 0:30 | Concepts: authentication vs authorization, tokens, RBAC, CORS |
| 0:30 – 1:20 | Live code: `utils.py`, `api/auth.py` (register, login, logout, me, admin ping) |
| 1:20 – 1:35 | Live code: JSON error handlers + CORS in `app.py` |
| 1:35 – 1:55 | Test everything in Postman / Thunder Client |
| 1:55 – 2:00 | Homework |

---

## Concepts in plain words

- **Authentication** = *who are you?* (email + password). **Authorization** = *what may you do?* (roles).
- **Token login** – after a correct password the server returns a long string (token). The frontend sends it back in a header on every request:
  `Authentication-Token: <token>`. The server does not need to remember sessions.
- **Flask-Security-Too gives us**
  - `hash_password()` / `verify_password()` – passwords are stored as bcrypt hashes, never plain text
  - `user.get_auth_token()` – creates the token
  - `@auth_required("token")` – rejects requests without a valid token (401)
  - `@roles_required("admin")` – rejects users without the role (403)
- **Logout with tokens** – a token cannot be "deleted". We change the user's `fs_uniquifier`, which makes all their old tokens invalid.
- **401 vs 403** – 401 = not logged in / bad token. 403 = logged in but not allowed.
- **CORS** – Vue runs on `localhost:5173`, Flask on `localhost:5000`. Different port = different *origin*, so the browser blocks the call unless Flask says "5173 is allowed". `flask-cors` adds those headers.

---

## Build steps

| # | File | What & why |
|---|---|---|
| 1 | `requirements.txt` | add `Flask-CORS` |
| 2 | `application/utils.py` | `error()`, `get_json(*required)` (reads body, trims strings, lists missing fields), `parse_date()`, `user_to_dict()` |
| 3 | `application/api/auth.py` | Blueprint with `/api/register`, `/api/login`, `/api/logout`, `/api/me`, `/api/admin/ping` |
| 4 | `app.py` | register blueprint, `CORS(...)`, custom 401/403 JSON handlers, 404 JSON handler |

Login in 6 lines (the heart of today):

```python
user = datastore.find_user(email=data["email"].lower())
if not user or not verify_password(data["password"], user.password):
    return error("Invalid email or password", 401)
if not user.active:
    return error("Your account is blocked. Contact admin.", 403)
return jsonify(token=user.get_auth_token(), user=user_to_dict(user))
```

Backend validation on register: required fields, email contains `@`, password ≥ 6 characters, duplicate email → 409.

Login also updates `last_visit` – the Day 6 reminder job uses it.

---

## Run & check (Postman / Thunder Client)

1. `POST /api/register` body `{"email":"a@b.com","password":"secret1","full_name":"Ann"}` → 201
2. `POST /api/login` with same email/password → copy `token`
3. `GET /api/me` without header → **401**; with header `Authentication-Token: <token>` → user JSON
4. `GET /api/admin/ping` with the user token → **403**; log in as admin and repeat → 200
5. `POST /api/logout` with the user token, then `GET /api/me` with the same token → **401**

## Common errors

| Error | Fix |
|---|---|
| Always 401 even with token | header name must be exactly `Authentication-Token` |
| HTML redirect instead of JSON | add the `unauthn_handler` / `unauthz_handler` from `app.py` |
| Error mentioning bcrypt / password hash | `pip install bcrypt` (it is in `requirements.txt`), keep `SECURITY_PASSWORD_HASH = "bcrypt"` |
| CORS error in the browser console | origin in `FRONTEND_ORIGIN` must match the Vue URL exactly |

## Homework

1. Add a `PUT /api/me` endpoint to update `full_name` and `qualification`.
2. Find where the token expiry is set (`SECURITY_TOKEN_MAX_AGE`) and try a 60-second expiry.
