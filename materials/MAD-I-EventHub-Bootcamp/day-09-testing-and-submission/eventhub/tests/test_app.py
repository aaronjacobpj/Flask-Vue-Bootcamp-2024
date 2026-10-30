"""Run all tests:  pytest -v"""
from conftest import login
from models import Booking, User, db


# ---------- pages and auth ----------

def test_home_page_lists_only_upcoming_events(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b"Future Gig" in response.data
    assert b"Past Gig" not in response.data


def test_admin_is_created_by_code(app):
    admin = User.query.filter_by(email=app.config["ADMIN_EMAIL"]).one()
    assert admin.is_admin
    assert admin.password_hash != app.config["ADMIN_PASSWORD"]  # stored as a hash


def test_register_then_login(client):
    response = client.post("/register", data={
        "name": "New Person", "email": "new@test.com", "password": "secret1", "confirm": "secret1",
    }, follow_redirects=True)
    assert b"Account created" in response.data

    response = login(client, "new@test.com", "secret1")
    assert b"Welcome, New Person" in response.data


def test_register_rejects_duplicate_email(client):
    response = client.post("/register", data={
        "name": "Copy", "email": "user@test.com", "password": "secret1", "confirm": "secret1",
    })
    assert b"already exists" in response.data


def test_wrong_password_is_rejected(client):
    response = login(client, "user@test.com", "wrong-password")
    assert b"Wrong email or password" in response.data


def test_flagged_user_cannot_log_in(client, app):
    user = User.query.filter_by(email="user@test.com").one()
    user.is_flagged = True
    db.session.commit()
    response = login(client, "user@test.com", "user123")
    assert b"flagged" in response.data


# ---------- role-based access ----------

def test_admin_pages_need_login(client):
    response = client.get("/admin/")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_user_cannot_open_admin_pages(user_client):
    assert user_client.get("/admin/").status_code == 403
    assert user_client.get("/admin/users").status_code == 403


def test_admin_can_open_admin_pages(admin_client):
    for url in ["/admin/", "/admin/users", "/admin/bookings", "/admin/summary", "/admin/search?q=gig"]:
        assert admin_client.get(url).status_code == 200, url


# ---------- admin CRUD ----------

def test_admin_creates_venue(admin_client):
    response = admin_client.post("/admin/venues/new", data={
        "name": "New Venue", "city": "Pune", "address": "", "capacity": "40",
    }, follow_redirects=True)
    assert b"New Venue" in response.data


def test_event_seats_cannot_exceed_capacity(admin_client, future_event):
    response = admin_client.post(f"/admin/events/{future_event.id}/edit", data={
        "venue_id": future_event.venue_id, "title": "Future Gig", "description": "",
        "date_time": "2030-01-01T10:00", "price": "100", "total_seats": "500",
    })
    assert b"cannot exceed the venue capacity" in response.data


# ---------- booking ----------

def test_user_books_seats(user_client, future_event):
    response = user_client.post(f"/events/{future_event.id}/book", data={"seats": "3"},
                                follow_redirects=True)
    assert b"Booked 3 seat(s)" in response.data
    assert future_event.seats_left == 7


def test_cannot_overbook(user_client, future_event):
    response = user_client.post(f"/events/{future_event.id}/book", data={"seats": "11"})
    assert b"Only 10 seat(s) left" in response.data
    assert Booking.query.count() == 0


def test_cannot_book_past_event(user_client, past_event):
    response = user_client.post(f"/events/{past_event.id}/book", data={"seats": "1"})
    assert b"already happened" in response.data


def test_cancel_frees_seats(user_client, future_event):
    user_client.post(f"/events/{future_event.id}/book", data={"seats": "4"})
    booking = Booking.query.one()
    user_client.post(f"/bookings/{booking.id}/cancel")
    assert booking.status == "cancelled"
    assert future_event.seats_left == 10


# ---------- API ----------

def test_api_lists_events(client):
    response = client.get("/api/events")
    assert response.status_code == 200
    assert {e["title"] for e in response.get_json()} == {"Future Gig", "Past Gig"}


def test_api_write_needs_admin(user_client):
    assert user_client.post("/api/venues", json={"name": "X", "city": "Y", "capacity": 5}).status_code == 403


def test_api_create_update_delete_venue(admin_client):
    response = admin_client.post("/api/venues", json={"name": "API Hall", "city": "Goa", "capacity": 30})
    assert response.status_code == 201
    venue_id = response.get_json()["id"]

    response = admin_client.put(f"/api/venues/{venue_id}", json={"capacity": 35})
    assert response.get_json()["capacity"] == 35

    assert admin_client.delete(f"/api/venues/{venue_id}").status_code == 204
    assert admin_client.get(f"/api/venues/{venue_id}").status_code == 404


def test_api_rejects_bad_data(admin_client):
    response = admin_client.post("/api/venues", json={"name": "", "city": "Goa", "capacity": 0})
    assert response.status_code == 400
    assert "required" in response.get_json()["message"]
