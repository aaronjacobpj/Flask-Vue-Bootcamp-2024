"""Public and user-side pages: browse, book, my bookings, cancel, summary."""
from datetime import datetime

from flask import Blueprint, abort, flash, redirect, render_template, request, url_for
from flask_login import current_user

from decorators import user_required
from models import Booking, Event, Venue, db

user_bp = Blueprint("user", __name__)


@user_bp.route("/")
def index():
    """Upcoming events, with an optional search box (?q=...). Open to everyone."""
    q = request.args.get("q", "").strip()
    query = Event.query.join(Venue).filter(Event.date_time >= datetime.now())
    if q:
        like = f"%{q}%"
        # ilike = case-insensitive LIKE. SQLAlchemy escapes the value: no SQL injection.
        query = query.filter(Event.title.ilike(like) | Venue.name.ilike(like) | Venue.city.ilike(like))
    events = query.order_by(Event.date_time).all()
    return render_template("index.html", events=events, q=q)


@user_bp.route("/events/<int:event_id>/book", methods=["GET", "POST"])
@user_required
def book(event_id):
    event = db.get_or_404(Event, event_id)

    if request.method == "POST":
        seats = request.form.get("seats", type=int)
        # Re-check everything on the server: the page may be old, or the form may be faked.
        if not event.is_upcoming:
            flash("This event has already happened.", "danger")
        elif seats is None or seats < 1:
            flash("Choose at least 1 seat.", "danger")
        elif seats > event.seats_left:
            flash(f"Only {event.seats_left} seat(s) left.", "danger")
        else:
            booking = Booking(user=current_user, event=event, seats=seats)
            db.session.add(booking)
            db.session.commit()
            flash(f"Booked {seats} seat(s) for {event.title}.", "success")
            return redirect(url_for("user.bookings"))

    return render_template("user/book.html", event=event)


@user_bp.route("/bookings")
@user_required
def bookings():
    my_bookings = (Booking.query.filter_by(user_id=current_user.id)
                   .order_by(Booking.booked_at.desc()).all())
    return render_template("user/bookings.html", bookings=my_bookings)


@user_bp.route("/bookings/<int:booking_id>/cancel", methods=["POST"])
@user_required
def cancel(booking_id):
    booking = db.get_or_404(Booking, booking_id)
    if booking.user_id != current_user.id:
        abort(403)  # users may only cancel their own bookings
    if booking.status != "booked" or not booking.event.is_upcoming:
        flash("This booking cannot be cancelled.", "warning")
    else:
        booking.status = "cancelled"
        db.session.commit()
        flash("Booking cancelled. The seats are free again.", "info")
    return redirect(url_for("user.bookings"))


@user_bp.route("/summary")
@user_required
def summary():
    my_bookings = Booking.query.filter_by(user_id=current_user.id).all()
    active = [b for b in my_bookings if b.status == "booked"]

    spend_by_venue = {}
    for b in active:
        spend_by_venue[b.event.venue.name] = spend_by_venue.get(b.event.venue.name, 0) + b.total_price

    status_counts = {
        "Upcoming": sum(1 for b in active if b.event.is_upcoming),
        "Attended": sum(1 for b in active if not b.event.is_upcoming),
        "Cancelled": sum(1 for b in my_bookings if b.status == "cancelled"),
    }
    return render_template(
        "user/summary.html",
        spend_chart={"labels": list(spend_by_venue), "values": list(spend_by_venue.values())},
        status_chart={"labels": list(status_counts), "values": list(status_counts.values())},
        total_spent=sum(spend_by_venue.values()),
        total_seats=sum(b.seats for b in active),
    )
