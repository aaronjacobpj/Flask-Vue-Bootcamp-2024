# Day 7 – Caching, summary charts & final review

**Goal:** faster APIs with Redis caching, summary charts for admin and user, and a project that is ready for submission and viva.

**By the end, students can**
- cache API responses with Flask-Caching and explain cache expiry & invalidation
- draw charts with ApexCharts (the `vue3-apexcharts` component) inside a Vue component
- walk through the whole app and answer common viva questions

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap of the whole stack |
| 0:10 – 0:45 | Caching: concept, `cache.cached`, `cache.memoize`, invalidation after writes, expiry |
| 0:45 – 1:15 | Summary API + `BarChart.vue` + admin & user summary pages |
| 1:15 – 1:35 | Security & quality checklist, responsive check on a phone |
| 1:35 – 2:00 | Full demo end-to-end, project report outline, viva questions |

---

## Caching in plain words

- A **cache** keeps the answer to a question so the next time we don't ask the database again.
- We store it in **Redis** (database number 2, separate from Celery's 0 and 1).
- **Expiry (timeout)** – every cached entry deletes itself after N seconds (`CACHE_DEFAULT_TIMEOUT = 300`; summaries use 60).
- **Invalidation** – when data changes, delete the old cached copy so nobody sees stale data.

| What is cached | How | Cleared when |
|---|---|---|
| `GET /api/subjects` (same for everyone) | `@cache.cached(key_prefix="subjects")` | any POST/PUT/DELETE in `resources.py` (one `after_request` hook) |
| quiz list (differs for admin/user) | `@cache.memoize()` on `quiz_list(include_empty)` | same hook: `cache.delete_memoized(quiz_list)` |
| `GET /api/admin/summary` | `@cache.cached(timeout=60, …)` | expires after 60 s |
| user summary (per user) | `@cache.memoize(timeout=60)` on `_user_summary(user_id)` | expires after 60 s |

Order of decorators matters: `@auth_required` **above** `@cache.cached`, so the token is checked *before* a cached answer is returned.

`app.py` calls `cache.clear()` on start, so deleting the database never leaves old data in Redis.

Show it live: `redis-cli -n 2 keys '*'` before and after opening the dashboard; time the request in DevTools (first call vs second call).

## Charts in plain words

- `npm install apexcharts vue3-apexcharts`
- Register it **once** in `main.js`: `import VueApexCharts from 'vue3-apexcharts'` then `app.use(VueApexCharts)`. Now every component can use `<apexchart>` without importing it.
- `components/BarChart.vue` – a tiny reusable wrapper around `<apexchart type="bar" :options="options" :series="series" />`. We only **describe** the chart: `series` (the numbers) and `options` (labels, colour, y-axis max) are two `computed` values built from the props. When the API answers, the props change, the computed values change and ApexCharts redraws by itself – no `watch`, no `mounted()`, no cleanup.
- `GET /api/admin/summary` → totals (users, subjects, quizzes, attempts) + per-subject attempts / average / best %, using one SQL `GROUP BY` query.
- Admin page: 4 stat cards + "Top score per subject" + "Attempts per subject".
- User page: "Average score per subject" + "Quizzes attempted per subject".

---

## Build steps

| # | File | What & why |
|---|---|---|
| 1 | `requirements.txt`, `config.py` | `Flask-Caching`, `CACHE_TYPE="RedisCache"`, `CACHE_REDIS_URL`, default timeout |
| 2 | `application/extensions.py`, `app.py` | `cache = Cache()`, `cache.init_app(app)`, `cache.clear()` on start, register `summary_bp` |
| 3 | `application/api/resources.py` | cache subjects & quiz list, `after_request` invalidation |
| 4 | `application/api/summary.py` | `_by_subject()` query, admin & user summary (cached 60 s) |
| 5 | `frontend`: `npm install apexcharts vue3-apexcharts` | |
| 6 | `main.js` (`app.use(VueApexCharts)`), `components/BarChart.vue`, `views/admin/AdminSummary.vue`, `views/user/UserSummary.vue` | |
| 7 | `router/index.js`, `NavBar.vue` | `/admin/summary`, `/summary` + "Summary" links |

---

## Security & quality checklist (go through it with students)

- [x] Passwords hashed with bcrypt (Flask-Security-Too); never returned in any API
- [x] Every non-public API has `@auth_required("token")`; admin APIs also `@roles_required("admin")`
- [x] Frontend route guards are only for UX – backend checks are the real protection
- [x] Correct answers never sent to users; score calculated on the server
- [x] Backend validation on every form + HTML5 validation in Vue
- [x] SQLAlchemy queries are parameterised (no string-built SQL)
- [x] CORS allows only the frontend origin
- [x] Users can download only their own export files
- [x] Blocked users cannot log in
- [ ] Before deploying: change `SECRET_KEY`, `SECURITY_PASSWORD_SALT`, admin password (environment variables)

## Optional extension – PDF monthly report

Install `xhtml2pdf`, convert the same `monthly_report.html` to PDF in `monthly_reports()` and attach it to the email (`email.mime.application.MIMEApplication`). Keep HTML as the default; let the user choose in their profile.

---

## Project report outline (for submission)

1. Student details
2. Problem statement & approach (2–3 lines)
3. Frameworks and libraries used (and why)
4. ER diagram (Day 1 homework)
5. API endpoints table (Day 3 homework / root README)
6. Features: core + optional (root README, section 3)
7. Demo video link (5–10 minutes: admin flow, user flow, jobs, caching)

## Viva question bank

1. Why does MAD II use a separate frontend instead of Jinja templates?
2. Session login vs token login – which do you use and how does the token reach the server?
3. How does logout work if tokens are not stored on the server? (`fs_uniquifier`)
4. 401 vs 403 – show an example of each in your app.
5. What happens if a user edits the frontend and opens `/admin`? Why is that still safe?
6. Explain the Vuex flow for logging in. Why mutations and actions separately?
7. Why is the token also stored in localStorage? Any risk?
8. What is CORS and why did you need it?
9. Explain your database design. What does `cascade="all, delete-orphan"` do?
10. How do you stop a user from seeing correct answers?
11. What is Celery? What is Redis doing for Celery? Worker vs beat?
12. How does the CSV export reach the user if it runs in the background?
13. When is the daily reminder sent and to whom?
14. What do you cache, for how long, and how do you avoid stale data?
15. How did you make the UI work on mobile?

---

## Final run

See the root `README.md`, section 5 – five terminals, then log in as admin and user.
