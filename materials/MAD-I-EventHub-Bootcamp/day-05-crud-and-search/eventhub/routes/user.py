"""Public and user-side pages."""
from datetime import datetime

from flask import Blueprint, render_template, request

from models import Event, Venue

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def index():
    """Upcoming events, with an optional search box (?q=...)."""
    q = request.args.get("q", "").strip()
    query = Event.query.join(Venue).filter(Event.date_time >= datetime.now())
    if q:
        like = f"%{q}%"
        # ilike = case-insensitive LIKE. SQLAlchemy escapes the value: no SQL injection.
        query = query.filter(Event.title.ilike(like) | Venue.name.ilike(like) | Venue.city.ilike(like))
    events = query.order_by(Event.date_time).all()
    return render_template("index.html", events=events, q=q)
