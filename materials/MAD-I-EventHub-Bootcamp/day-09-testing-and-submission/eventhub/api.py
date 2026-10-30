"""REST API for venues and events, built with Flask-RESTful.

    GET     /api/venues            list venues            (anyone)
    POST    /api/venues            create a venue         (admin)
    GET     /api/venues/<id>       one venue + its events (anyone)
    PUT     /api/venues/<id>       update a venue         (admin)
    DELETE  /api/venues/<id>       delete a venue         (admin)
    (the same five for /api/events)

Admin calls use the normal login session cookie: log in first (browser, Postman or curl).
"""
from datetime import datetime

from flask import Blueprint, request
from flask_login import current_user
from flask_restful import Api, Resource, abort

from models import Event, Venue, db

api_bp = Blueprint("api", __name__, url_prefix="/api")
api = Api(api_bp)


# ---------- helpers ----------

def require_admin():
    if not current_user.is_authenticated:
        abort(401, message="Log in first.")
    if not current_user.is_admin:
        abort(403, message="Admin only.")


def get_json():
    data = request.get_json(silent=True)
    if not isinstance(data, dict):
        abort(400, message="Send a JSON object with Content-Type: application/json.")
    return data


def venue_to_dict(venue, with_events=False):
    data = {"id": venue.id, "name": venue.name, "city": venue.city,
            "address": venue.address, "capacity": venue.capacity}
    if with_events:
        data["events"] = [event_to_dict(e) for e in venue.events]
    return data


def event_to_dict(event):
    return {
        "id": event.id,
        "title": event.title,
        "description": event.description,
        "venue_id": event.venue_id,
        "venue": event.venue.name,
        "date_time": event.date_time.isoformat(timespec="minutes"),
        "price": event.price,
        "total_seats": event.total_seats,
        "seats_left": event.seats_left,
    }


def apply_venue_data(venue, data):
    """Copy allowed fields from JSON into the venue. Returns a list of error messages."""
    for field in ("name", "city", "address"):
        if field in data:
            setattr(venue, field, str(data[field] or "").strip())
    if "capacity" in data:
        venue.capacity = data["capacity"]

    errors = []
    if not venue.name or not venue.city:
        errors.append("name and city are required.")
    if not isinstance(venue.capacity, int) or venue.capacity < 1:
        errors.append("capacity must be a whole number above 0.")
    elif venue.events and venue.capacity < max(e.total_seats for e in venue.events):
        errors.append("capacity cannot be less than the seats of an existing event here.")
    return errors


def apply_event_data(event, data):
    errors = []
    if "venue_id" in data:
        event.venue = db.session.get(Venue, data["venue_id"]) if isinstance(data["venue_id"], int) else None
    for field in ("title", "description"):
        if field in data:
            setattr(event, field, str(data[field] or "").strip())
    if "date_time" in data:
        try:
            event.date_time = datetime.fromisoformat(str(data["date_time"]))
        except ValueError:
            errors.append("date_time must look like 2026-12-31T19:30.")
    if "price" in data:
        event.price = data["price"]
    if "total_seats" in data:
        event.total_seats = data["total_seats"]

    if event.venue is None:
        errors.append("venue_id must be an existing venue id.")
    if not event.title:
        errors.append("title is required.")
    if event.date_time is None and not errors:
        errors.append("date_time is required.")
    if not isinstance(event.price, (int, float)) or event.price < 0:
        errors.append("price must be a number, 0 or more.")
    if not isinstance(event.total_seats, int) or event.total_seats < 1:
        errors.append("total_seats must be a whole number above 0.")
    elif event.venue and event.total_seats > event.venue.capacity:
        errors.append(f"total_seats cannot exceed the venue capacity ({event.venue.capacity}).")
    elif event.id and event.total_seats < event.seats_booked:
        errors.append(f"{event.seats_booked} seats are already booked.")
    return errors


# ---------- resources ----------

class VenueListAPI(Resource):
    def get(self):
        return [venue_to_dict(v) for v in Venue.query.order_by(Venue.name).all()]

    def post(self):
        require_admin()
        venue = Venue()
        errors = apply_venue_data(venue, get_json())
        if errors:
            abort(400, message=" ".join(errors))
        db.session.add(venue)
        db.session.commit()
        return venue_to_dict(venue), 201  # 201 Created


class VenueAPI(Resource):
    def get(self, venue_id):
        return venue_to_dict(db.get_or_404(Venue, venue_id), with_events=True)

    def put(self, venue_id):
        require_admin()
        venue = db.get_or_404(Venue, venue_id)
        errors = apply_venue_data(venue, get_json())
        if errors:
            db.session.rollback()  # undo the changes we copied in
            abort(400, message=" ".join(errors))
        db.session.commit()
        return venue_to_dict(venue)

    def delete(self, venue_id):
        require_admin()
        venue = db.get_or_404(Venue, venue_id)
        db.session.delete(venue)
        db.session.commit()
        return "", 204  # 204 No Content


class EventListAPI(Resource):
    def get(self):
        query = Event.query.order_by(Event.date_time)
        if request.args.get("upcoming") == "1":
            query = query.filter(Event.date_time >= datetime.now())
        return [event_to_dict(e) for e in query.all()]

    def post(self):
        require_admin()
        event = Event()
        errors = apply_event_data(event, get_json())
        if errors:
            db.session.rollback()
            abort(400, message=" ".join(errors))
        db.session.add(event)
        db.session.commit()
        return event_to_dict(event), 201


class EventAPI(Resource):
    def get(self, event_id):
        return event_to_dict(db.get_or_404(Event, event_id))

    def put(self, event_id):
        require_admin()
        event = db.get_or_404(Event, event_id)
        errors = apply_event_data(event, get_json())
        if errors:
            db.session.rollback()
            abort(400, message=" ".join(errors))
        db.session.commit()
        return event_to_dict(event)

    def delete(self, event_id):
        require_admin()
        event = db.get_or_404(Event, event_id)
        db.session.delete(event)
        db.session.commit()
        return "", 204


api.add_resource(VenueListAPI, "/venues")
api.add_resource(VenueAPI, "/venues/<int:venue_id>")
api.add_resource(EventListAPI, "/events")
api.add_resource(EventAPI, "/events/<int:event_id>")
