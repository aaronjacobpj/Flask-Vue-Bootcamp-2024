# Day 8 – REST APIs, JavaScript and summary charts

**Goal:** EventHub exposes venues and events as a JSON API, and both roles get a summary page with charts.

**By the end, students can**
- explain REST: resources, HTTP verbs, JSON, status codes
- build CRUD endpoints with Flask-RESTful and test them in Postman or curl
- use a little JavaScript: live form feedback and `fetch()` from their own API
- pass data from Flask to Chart.js safely with `tojson`

BSCS2003 weeks covered: 6 (APIs and REST APIs), 7 (backend systems), 8 (application frontend).

---

## Agenda (2 hours)

| Time | Activity |
|---|---|
| 0:00 – 0:10 | Recap; what an API is and who calls it (other apps, JavaScript, Postman) |
| 0:10 – 0:25 | REST on the whiteboard: URL = noun, verb = action, status codes |
| 0:25 – 1:00 | Live code: `api.py` – venues list/detail, then events; test each in Postman |
| 1:00 – 1:20 | Live code: admin summary page with Chart.js; `app.js` (booking total + `fetch`) |
| 1:20 – 1:50 | Hands-on: one CRUD API and one summary page per student |
| 1:50 – 2:00 | Recap, homework |

---

## Concepts in plain words

- **REST** – the URL names a *thing*, the method says what to do with it:

  | Method | `/api/venues` | `/api/venues/3` |
  |---|---|---|
  | GET | list all | get one |
  | POST | create one | – |
  | PUT | – | update it |
  | DELETE | – | delete it |

- **Status codes the API returns** – `200` OK, `201` Created, `204` No Content (deleted), `400` bad input, `401` not logged in, `403` not allowed, `404` not found.
- **Flask-RESTful** – a `Resource` class with `get`, `post`, `put`, `delete` methods; return a dict or list and it becomes JSON. `abort(400, message="...")` sends a JSON error.
- **Serialising** – a model object is not JSON. `event_to_dict()` picks the fields to expose (never `password_hash`).
- **API security** – the same session cookie works for API calls; write endpoints call `require_admin()`.
- **`fetch()`** – JavaScript asks the server for JSON without reloading the page. The booking page uses it to show the latest seat count.
- **JavaScript is optional polish** – the app must work with JS turned off. Every JS check is repeated on the server.
- **Charts** – compute the numbers in Python, pass them with `{{ data | tojson }}`, let Chart.js draw. `tojson` escapes the data safely.
- **Choosing a chart** – parts of one total (booked + free seats) → stacked bar; share of a whole (revenue by venue) → doughnut; comparing amounts → bar.

---

## Live-coding script

| # | Do | Say / show |
|---|---|---|
| 1 | `pip install flask-restful`; `api.py` with `api_bp` + `Api(api_bp)`; register in `create_app` | The API lives under `/api` |
| 2 | `venue_to_dict`, `VenueListAPI.get` | Open `/api/venues` in the browser – JSON |
| 3 | `VenueAPI.get` with `with_events=True` | Nested JSON from relationships |
| 4 | `VenueListAPI.post` with `get_json()` and validation → `201` | Postman: Body → raw → JSON. Show `400` for bad input |
| 5 | `require_admin()`; try POST logged out (`401`) and as Priya (`403`) | Log in through `/login` in Postman first – it keeps the cookie |
| 6 | `put` (partial update) and `delete` (`204`) | `db.session.rollback()` undoes changes when validation fails |
| 7 | Events resources – same pattern, show `?upcoming=1` | Reuse, don't reinvent |
| 8 | `routes/admin.py` `summary()` builds lists; `admin/summary.html` with Chart.js | View source: see the JSON `tojson` produced |
| 9 | `static/js/app.js`: `drawChart` helper, booking total, `fetch('/api/events/<id>')` | DevTools → Network shows the fetch call |
| 10 | User summary page | Same helper, different data |

## API test sheet (curl)

```bash
# public
curl http://127.0.0.1:5000/api/venues
curl "http://127.0.0.1:5000/api/events?upcoming=1"

# log in as admin and keep the cookie
curl -c cookies.txt -d "email=admin@eventhub.com&password=admin123" http://127.0.0.1:5000/login

# create, update, delete
curl -b cookies.txt -H "Content-Type: application/json" \
     -d '{"name": "Town Hall", "city": "Pune", "capacity": 200}' http://127.0.0.1:5000/api/venues
curl -b cookies.txt -X PUT -H "Content-Type: application/json" \
     -d '{"capacity": 250}' http://127.0.0.1:5000/api/venues/4
curl -b cookies.txt -X DELETE -i http://127.0.0.1:5000/api/venues/4
```

---

## Run & check

```bash
cd eventhub
source .venv/bin/activate
pip install -r requirements.txt     # adds Flask-RESTful
python app.py
```

- `/api/venues`, `/api/events/1` return JSON. POST without login → `401` JSON.
- Admin → Summary: stacked bar of seats and a revenue doughnut. Priya → Summary: spending and status charts.
- Booking page: changing seats updates the total immediately.

## Common errors

| Error | Fix |
|---|---|
| `TypeError: Object of type datetime is not JSON serializable` | convert with `.isoformat()` in the `to_dict` function |
| `400 Bad Request` / `get_json()` returns `None` | Postman body must be **raw → JSON**, header `Content-Type: application/json` |
| API returns HTML login page instead of JSON | the API route uses `@login_required`; use `require_admin()` returning JSON errors |
| `404` for `/api/venues` | blueprint not registered, or `url_prefix` typo |
| Chart area blank | Chart.js `<script>` missing or loaded after your code; check the DevTools console |
| `Uncaught SyntaxError` in the chart script | data printed without `| tojson` |
| `fetch` shows CORS error | you opened the HTML file directly – use the Flask URL |

## Homework

1. Finish the API your project statement asks for and test every endpoint (keep the Postman collection or curl list for the report).
2. Add the summary charts your project asks for.
3. Polish the UI and fix every open bug.
