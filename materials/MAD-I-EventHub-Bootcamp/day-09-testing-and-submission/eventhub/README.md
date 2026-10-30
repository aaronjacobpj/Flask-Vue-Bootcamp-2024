# EventHub

A multi-user event-booking web app built with Flask, Jinja2, SQLite and Bootstrap.
The admin manages venues and events; users register, browse, search and book seats.

## Features

| Role | Can do |
|---|---|
| Admin (created automatically, no sign-up) | Create, edit and delete venues and events; view all bookings; search users, venues and events; flag or unflag users; see summary charts |
| User | Register and log in; browse and search upcoming events; book seats; cancel a booking; view booking history and a personal summary |

A REST API (`/api/venues`, `/api/events`) exposes the same data as JSON.

## Run it

Requires Python 3.10 or newer.

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python seed_demo.py              # optional: demo venues, events, users and bookings
python app.py                    # open http://127.0.0.1:5000
```

The database (`instance/eventhub.db`) and the admin account are created by code on first run.

| Account | Email | Password |
|---|---|---|
| Admin | admin@eventhub.com | admin123 |
| Demo user (after `seed_demo.py`) | priya@example.com | user123 |

To start with an empty database, stop the app and delete `instance/eventhub.db`.

## Run the tests

```bash
pytest -v
```

## Project structure

```
eventhub/
├── app.py            # create_app(): config, database, login manager, blueprints, error pages
├── config.py         # Config and TestConfig
├── models.py         # User, Venue, Event, Booking
├── seed.py           # creates the admin on startup
├── seed_demo.py      # optional demo data
├── decorators.py     # admin_required, user_required
├── api.py            # Flask-RESTful resources
├── routes/
│   ├── auth.py       # register, login, logout
│   ├── admin.py      # dashboard, CRUD, users, bookings, search, summary
│   └── user.py       # browse, book, my bookings, cancel, summary
├── templates/        # base.html, index.html, error.html, auth/, admin/, user/
├── static/           # css/style.css, js/app.js
└── tests/            # pytest tests
```

## Database

```
User ──< Booking >── Event >── Venue
```

| Table | Columns |
|---|---|
| user | id, name, email (unique), password_hash, role (`admin` / `user`), is_flagged, created_at |
| venue | id, name, city, address, capacity |
| event | id, venue_id → venue, title, description, date_time, price, total_seats |
| booking | id, user_id → user, event_id → event, seats, booked_at, status (`booked` / `cancelled`) |

Seats left is calculated from bookings (`total_seats` minus booked seats), so it never goes out of sync.

## API

| Method | URL | Who | Purpose |
|---|---|---|---|
| GET | `/api/venues` | anyone | List venues |
| POST | `/api/venues` | admin | Create a venue |
| GET | `/api/venues/<id>` | anyone | One venue with its events |
| PUT | `/api/venues/<id>` | admin | Update a venue (send only the fields to change) |
| DELETE | `/api/venues/<id>` | admin | Delete a venue and its events |
| GET | `/api/events` (`?upcoming=1`) | anyone | List events |
| POST | `/api/events` | admin | Create an event |
| GET | `/api/events/<id>` | anyone | One event, including `seats_left` |
| PUT | `/api/events/<id>` | admin | Update an event |
| DELETE | `/api/events/<id>` | admin | Delete an event |

Admin requests use the login session cookie. With curl:

```bash
curl -c cookies.txt -d "email=admin@eventhub.com&password=admin123" http://127.0.0.1:5000/login
curl -b cookies.txt -H "Content-Type: application/json" \
     -d '{"name": "Town Hall", "city": "Pune", "capacity": 200}' \
     http://127.0.0.1:5000/api/venues
```

## Technologies

Flask, Flask-SQLAlchemy, Flask-Login, Flask-RESTful, Jinja2, SQLite, Bootstrap 5, Chart.js, pytest.
