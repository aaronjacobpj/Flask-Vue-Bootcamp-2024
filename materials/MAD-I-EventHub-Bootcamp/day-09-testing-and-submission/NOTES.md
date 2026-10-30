# Day 9 – Testing, deployment, report and video

**Goal:** EventHub is submittable: tested, runs from a fresh clone, documented, with a report and a video plan.

**By the end, students can**
- write a manual test checklist and a few `pytest` tests with Flask's test client
- make the project run on any machine: `requirements.txt`, README, `.gitignore`, no hard-coded paths
- structure the project report and plan a short demo video

BSCS2003 weeks covered: 10 (testing), 11 (HTML evolution and beyond), 12 (deployment).

`eventhub/` in this folder is the **finished project**.

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap; show the final app end to end, both roles |
| 0:10 – 0:30 | Testing: manual checklist, then `pytest` with `TestConfig` and fixtures |
| 0:30 – 0:50 | Live code: 4–5 tests (auth, 403, booking rules, API) |
| 0:50 – 1:05 | Fresh-clone test: clone the repo into a new folder and run it from the README only |
| 1:05 – 1:20 | Report structure (`REPORT-TEMPLATE.md`) and video plan (`VIDEO-SCRIPT.md`); deployment options in brief |
| 1:20 – 1:50 | Hands-on: students write their report draft and video script |
| 1:50 – 2:00 | Homework: record a practice video; questions for Day 10 |

---

## Concepts in plain words

- **Manual test checklist** – a table of *page / action / expected result*. Walk through it before every submission.
- **Automated tests** – code that checks code. `app.test_client()` sends fake requests without a browser.
- **`TestConfig`** – an in-memory database, so tests never touch your real data and start fresh each time.
- **Fixtures** (`tests/conftest.py`) – shared setup pytest passes into tests: `client`, `user_client`, `admin_client`, `future_event`.
- **Arrange, act, assert** – set up data, do one thing, check the result.
- **Fresh-clone test** – the grader's machine has nothing but your zip. If it does not run from the README, it does not run.
- **Pinned requirements** – `Flask==3.1.3` instead of `Flask` means the same versions everywhere.
- **Deployment, briefly** – production uses a real WSGI server (gunicorn / waitress), `debug=False`, a secret key from the environment. Hosting is optional for MAD I; follow the project statement.
- **HTML beyond the page (week 11)** – mention responsive design, accessibility (labels, alt text, contrast) and progressive enhancement: the app works without JS.

## Manual test checklist (sample)

| # | As | Action | Expected |
|---|---|---|---|
| 1 | visitor | open `/admin/` | redirected to login |
| 2 | visitor | register with an existing email | error, form keeps values |
| 3 | user | book more seats than left | error, nothing booked |
| 4 | user | book 2 seats | success; seats left drops by 2 |
| 5 | user | cancel the booking | status cancelled; seats return |
| 6 | user | open `/admin/` | 403 page |
| 7 | admin | create an event with seats > capacity | error |
| 8 | admin | delete a venue | its events disappear |
| 9 | admin | flag a user | that user cannot log in |
| 10 | anyone | `GET /api/events` | JSON list |

---

## Live-coding script

| # | Do | Say / show |
|---|---|---|
| 1 | Add `TestConfig` to `config.py` | `create_app(TestConfig)` – this is why we built a factory on Day 3 |
| 2 | `pytest.ini` with `pythonpath = .` | So tests can `import app` |
| 3 | `tests/conftest.py`: `app`, `client`, `login` helper, role clients | Fixtures run before each test that names them |
| 4 | First test: home page lists upcoming, not past events | `pytest -v` – green |
| 5 | Break the code on purpose (remove the date filter) and rerun | Red test = the safety net works. Undo |
| 6 | Tests for 403, overbooking, cancel, API 201/204/400 | One behaviour per test |
| 7 | `pip freeze` → keep only what you use, pin versions | Remove packages you don't import |
| 8 | Write README: features, run steps, accounts, structure, API table | It doubles as the report's appendix |
| 9 | Fresh clone into `/tmp`, follow README exactly | Fix anything the README forgot |

---

## Run & check

```bash
cd eventhub
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
pytest -v                  # 19 tests pass
python seed_demo.py        # optional demo data
python app.py
```

## Common errors

| Error | Fix |
|---|---|
| `ModuleNotFoundError: No module named 'app'` in pytest | add `pytest.ini` with `pythonpath = .`, run `pytest` from the project folder |
| Tests change the real database | tests must use `create_app(TestConfig)` with `sqlite:///:memory:` |
| Tests pass alone, fail together | a test depends on another's data – each test must set up its own |
| `DetachedInstanceError` in a test | read model attributes inside the app context (the `app` fixture keeps one open) |
| Fresh clone fails: missing package | it is imported but not in `requirements.txt` |
| Fresh clone fails: file not found | absolute path like `C:/Users/...` in code – use relative paths |

## Homework

1. Write your report from `REPORT-TEMPLATE.md`.
2. Record a practice video following `VIDEO-SCRIPT.md`; watch it once and note what to fix.
3. Do the fresh-clone test on your own project.
4. Bring your last questions to Day 10.
