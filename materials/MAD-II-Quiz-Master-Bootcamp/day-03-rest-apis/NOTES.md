# Day 3 – REST APIs for the whole app

**Goal:** every feature of Quiz Master works through the API (tested in Postman) before we write any UI.

**By the end, students can**
- design REST URLs for nested resources (subject → chapter → quiz → question)
- write CRUD endpoints with validation and correct status codes
- explain why scoring must happen on the server

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap: token + roles |
| 0:10 – 0:25 | REST design on the board: URLs, methods, status codes |
| 0:25 – 1:05 | Live code: `serializers.py`, `api/resources.py` (subjects + chapters fully, quizzes + questions quickly – same pattern) |
| 1:05 – 1:25 | Live code: `api/user.py` (attempt, submit, scores) |
| 1:25 – 1:45 | Live code: `api/admin.py` (users, block, search) + `seed_demo.py` |
| 1:45 – 2:00 | Postman walk-through, homework |

---

## Concepts in plain words

- **REST** – a URL names a *thing*, the HTTP method says *what to do*:
  `GET` read · `POST` create · `PUT` update · `DELETE` remove.
- **Nested URLs** show ownership: `POST /api/subjects/3/chapters` = "create a chapter inside subject 3".
- **Status codes** we use: 200 OK, 201 Created, 400 bad input, 401 not logged in, 403 not allowed, 404 not found, 409 duplicate.
- **Serializer** – a small function that turns a model object into a dict (`subject_to_dict`). Keeps routes short and output consistent.
- **Never trust the client** – the attempt API sends questions **without** `correct_option`; the submit API calculates the score on the server.
- **Blueprint-wide protection** – in `admin.py`, `@admin_bp.before_request` runs before every admin route, so we protect the whole blueprint in one place (OPTIONS pre-flight requests are let through for CORS).

---

## Build steps

| # | File | What & why |
|---|---|---|
| 1 | `application/serializers.py` | `subject_to_dict` (optionally with chapters), `chapter_to_dict`, `quiz_to_dict`, `question_to_dict(with_answer)`, `score_to_dict` |
| 2 | `application/api/resources.py` | CRUD for subjects, chapters, quizzes, questions. `admin_only` = token + admin role. Validation helpers `_quiz_fields`, `_question_fields` |
| 3 | `application/api/user.py` | `GET /quizzes/<id>/attempt`, `POST /quizzes/<id>/submit`, `GET /scores` |
| 4 | `application/api/admin.py` | `GET /admin/users`, `PATCH /admin/users/<id>/toggle`, `GET /admin/scores`, `GET /admin/search?q=` |
| 5 | `app.py` | register the 3 new blueprints |
| 6 | `seed_demo.py` | 2 subjects, 4 chapters, 4 quizzes, demo user – so the UI has data |

Scoring (from `user.py`):

```python
for q in quiz.questions:
    chosen = answers.get(str(q.id))
    if chosen is not None and str(chosen) == str(q.correct_option):
        correct += 1
```

Validation examples: question needs ≥ 2 options and `correct_option` must point to a filled option; quiz `time_duration` must be a positive number; date must be `YYYY-MM-DD`.

Search uses `ilike("%text%")` – SQLAlchemy passes it as a parameter, so it is safe from SQL injection.

---

## Run & check

```bash
python seed_demo.py     # once
python app.py
```

Postman flow (admin token):
1. `POST /api/subjects` `{"name":"Maths"}` → 201
2. `POST /api/subjects/<id>/chapters` `{"name":"Algebra"}`
3. `POST /api/chapters/<id>/quizzes` `{"title":"Algebra Q1","time_duration":5,"date_of_quiz":"2026-11-01"}`
4. `POST /api/quizzes/<id>/questions` `{"statement":"1+1?","options":["1","2","3","4"],"correct_option":2}`
5. With a **user** token: `GET /api/quizzes/<id>/attempt` (no answers!) → `POST /api/quizzes/<id>/submit` `{"answers":{"<question_id>":2}}` → score
6. `GET /api/scores`, `GET /api/admin/search?q=alg`
7. Try `POST /api/subjects` with a user token → 403

## Common errors

| Error | Fix |
|---|---|
| `405 Method Not Allowed` | wrong HTTP method for that URL |
| Submit always gives 0 | answer keys must be question ids **as strings**: `{"5": 2}` |
| `sqlite3.IntegrityError UNIQUE` | duplicate subject name – we return 409 before inserting |
| Deleting a subject fails | missing `cascade="all, delete-orphan"` in models |

## Homework

1. Add `GET /api/quizzes/<id>/scores` for the admin (all attempts for one quiz).
2. Write down every endpoint with method, URL, role and body – this is the API section of the project report.
