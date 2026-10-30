"""Shared pytest fixtures. A fixture is a helper that pytest passes into any test that names it."""
from datetime import datetime, timedelta

import pytest

from app import create_app
from config import TestConfig
from models import Event, User, Venue, db


@pytest.fixture
def app():
    app = create_app(TestConfig)  # in-memory database, admin seeded automatically
    with app.app_context():
        user = User(name="Test User", email="user@test.com")
        user.set_password("user123")
        venue = Venue(name="Test Hall", city="Chennai", capacity=50)
        future = Event(title="Future Gig", venue=venue, price=100, total_seats=10,
                       date_time=datetime.now() + timedelta(days=7))
        past = Event(title="Past Gig", venue=venue, price=100, total_seats=10,
                     date_time=datetime.now() - timedelta(days=7))
        db.session.add_all([user, venue, future, past])
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


def login(client, email, password):
    return client.post("/login", data={"email": email, "password": password}, follow_redirects=True)


@pytest.fixture
def user_client(client):
    login(client, "user@test.com", "user123")
    return client


@pytest.fixture
def admin_client(client, app):
    login(client, app.config["ADMIN_EMAIL"], app.config["ADMIN_PASSWORD"])
    return client


@pytest.fixture
def future_event(app):
    return Event.query.filter_by(title="Future Gig").one()


@pytest.fixture
def past_event(app):
    return Event.query.filter_by(title="Past Gig").one()
