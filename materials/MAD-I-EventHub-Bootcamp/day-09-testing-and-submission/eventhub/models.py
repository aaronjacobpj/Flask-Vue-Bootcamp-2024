"""Database models (tables) for EventHub.

    User ──< Booking >── Event >── Venue
    (a user has many bookings, an event has many bookings, a venue has many events)
"""
from datetime import datetime

from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import check_password_hash, generate_password_hash

db = SQLAlchemy()


class User(db.Model, UserMixin):  # UserMixin is used by Flask-Login on Day 6
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(10), nullable=False, default="user")  # "admin" or "user"
    is_flagged = db.Column(db.Boolean, nullable=False, default=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now)

    bookings = db.relationship("Booking", back_populates="user", cascade="all, delete-orphan")

    def set_password(self, password):
        # Never store the password itself, only a salted hash of it.
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == "admin"


class Venue(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(60), nullable=False)
    address = db.Column(db.String(200))
    capacity = db.Column(db.Integer, nullable=False)

    # Deleting a venue deletes its events (and, through Event, their bookings).
    events = db.relationship("Event", back_populates="venue", cascade="all, delete-orphan",
                             order_by="Event.date_time")


class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    venue_id = db.Column(db.Integer, db.ForeignKey("venue.id"), nullable=False)
    title = db.Column(db.String(120), nullable=False)
    description = db.Column(db.Text)
    date_time = db.Column(db.DateTime, nullable=False)
    price = db.Column(db.Float, nullable=False, default=0)
    total_seats = db.Column(db.Integer, nullable=False)

    venue = db.relationship("Venue", back_populates="events")
    bookings = db.relationship("Booking", back_populates="event", cascade="all, delete-orphan")

    # Seats left is *calculated* from bookings instead of stored,
    # so it can never go out of sync.
    @property
    def seats_booked(self):
        return sum(b.seats for b in self.bookings if b.status == "booked")

    @property
    def seats_left(self):
        return self.total_seats - self.seats_booked

    @property
    def is_upcoming(self):
        return self.date_time > datetime.now()


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    event_id = db.Column(db.Integer, db.ForeignKey("event.id"), nullable=False)
    seats = db.Column(db.Integer, nullable=False)
    booked_at = db.Column(db.DateTime, nullable=False, default=datetime.now)
    status = db.Column(db.String(10), nullable=False, default="booked")  # "booked" or "cancelled"

    user = db.relationship("User", back_populates="bookings")
    event = db.relationship("Event", back_populates="bookings")

    @property
    def total_price(self):
        return self.seats * self.event.price
