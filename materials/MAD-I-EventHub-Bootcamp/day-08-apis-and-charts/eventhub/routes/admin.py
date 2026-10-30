"""Admin pages: dashboard, venues and events CRUD, users, bookings, search.

Every route has @admin_required: hiding a link in the navbar is NOT security.
"""
from datetime import datetime

from flask import Blueprint, flash, redirect, render_template, request, url_for

from decorators import admin_required
from models import Booking, Event, User, Venue, db

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


@admin_bp.route("/")
@admin_required
def dashboard():
    venues = Venue.query.order_by(Venue.name).all()
    stats = {
        "users": User.query.filter_by(role="user").count(),
        "venues": len(venues),
        "events": Event.query.count(),
        "bookings": Booking.query.filter_by(status="booked").count(),
    }
    return render_template("admin/dashboard.html", venues=venues, stats=stats)


# ---------- Venues ----------

@admin_bp.route("/venues/new", methods=["GET", "POST"])
@admin_required
def new_venue():
    return venue_form(Venue())


@admin_bp.route("/venues/<int:venue_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_venue(venue_id):
    return venue_form(db.get_or_404(Venue, venue_id))


def venue_form(venue):
    """One function handles both 'new' and 'edit'. GET shows the form, POST saves it."""
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        city = request.form.get("city", "").strip()
        address = request.form.get("address", "").strip()
        capacity = request.form.get("capacity", type=int)  # None if not a number

        errors = []
        if not name or not city:
            errors.append("Name and city are required.")
        if capacity is None or capacity < 1:
            errors.append("Capacity must be a whole number above 0.")
        elif venue.events and capacity < max(e.total_seats for e in venue.events):
            errors.append("Capacity cannot be less than the seats of an existing event here.")

        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            venue.name, venue.city, venue.address, venue.capacity = name, city, address, capacity
            if venue.id is None:
                db.session.add(venue)
            db.session.commit()
            flash(f"Venue '{venue.name}' saved.", "success")
            # Post/Redirect/Get: after a POST, redirect so a page refresh does not resubmit.
            return redirect(url_for("admin.dashboard"))

    return render_template("admin/venue_form.html", venue=venue)


@admin_bp.route("/venues/<int:venue_id>/delete", methods=["POST"])
@admin_required
def delete_venue(venue_id):
    venue = db.get_or_404(Venue, venue_id)
    db.session.delete(venue)  # cascade also deletes its events and their bookings
    db.session.commit()
    flash(f"Venue '{venue.name}' and its events deleted.", "info")
    return redirect(url_for("admin.dashboard"))


# ---------- Events ----------

@admin_bp.route("/events/new", methods=["GET", "POST"])
@admin_required
def new_event():
    event = Event(venue_id=request.args.get("venue_id", type=int))
    return event_form(event)


@admin_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@admin_required
def edit_event(event_id):
    return event_form(db.get_or_404(Event, event_id))


def event_form(event):
    venues = Venue.query.order_by(Venue.name).all()
    if not venues:
        flash("Create a venue first.", "warning")
        return redirect(url_for("admin.new_venue"))

    if request.method == "POST":
        venue = db.session.get(Venue, request.form.get("venue_id", type=int) or 0)
        title = request.form.get("title", "").strip()
        description = request.form.get("description", "").strip()
        price = request.form.get("price", type=float)
        total_seats = request.form.get("total_seats", type=int)
        try:
            date_time = datetime.fromisoformat(request.form.get("date_time", ""))
        except ValueError:
            date_time = None

        errors = []
        if venue is None:
            errors.append("Choose a venue.")
        if not title:
            errors.append("Title is required.")
        if date_time is None:
            errors.append("Enter a valid date and time.")
        if price is None or price < 0:
            errors.append("Price must be 0 or more.")
        if total_seats is None or total_seats < 1:
            errors.append("Seats must be a whole number above 0.")
        elif venue and total_seats > venue.capacity:
            errors.append(f"Seats cannot exceed the venue capacity ({venue.capacity}).")
        elif event.id and total_seats < event.seats_booked:
            errors.append(f"{event.seats_booked} seats are already booked; seats cannot be lower.")

        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            event.venue = venue
            event.title, event.description = title, description
            event.date_time, event.price, event.total_seats = date_time, price, total_seats
            if event.id is None:
                db.session.add(event)
            db.session.commit()
            flash(f"Event '{event.title}' saved.", "success")
            return redirect(url_for("admin.dashboard"))

    return render_template("admin/event_form.html", event=event, venues=venues)


@admin_bp.route("/events/<int:event_id>/delete", methods=["POST"])
@admin_required
def delete_event(event_id):
    event = db.get_or_404(Event, event_id)
    db.session.delete(event)
    db.session.commit()
    flash(f"Event '{event.title}' deleted.", "info")
    return redirect(url_for("admin.dashboard"))


# ---------- Users and bookings ----------

@admin_bp.route("/users")
@admin_required
def users():
    all_users = User.query.filter_by(role="user").order_by(User.created_at.desc()).all()
    return render_template("admin/users.html", users=all_users)


@admin_bp.route("/users/<int:user_id>/toggle-flag", methods=["POST"])
@admin_required
def toggle_flag(user_id):
    user = db.get_or_404(User, user_id)
    if user.is_admin:
        flash("The admin cannot be flagged.", "danger")
    else:
        user.is_flagged = not user.is_flagged
        db.session.commit()
        flash(f"{user.name} is now {'flagged' if user.is_flagged else 'active'}.", "info")
    return redirect(request.referrer or url_for("admin.users"))


@admin_bp.route("/bookings")
@admin_required
def bookings():
    all_bookings = Booking.query.order_by(Booking.booked_at.desc()).all()
    return render_template("admin/bookings.html", bookings=all_bookings)


# ---------- Summary (charts) ----------

@admin_bp.route("/summary")
@admin_required
def summary():
    events = Event.query.order_by(Event.date_time).all()
    venues = Venue.query.order_by(Venue.name).all()

    # Build simple lists in Python; the template hands them to Chart.js as JSON.
    seats_chart = {
        "labels": [e.title for e in events],
        "booked": [e.seats_booked for e in events],
        "left": [e.seats_left for e in events],
    }
    revenue_chart = {
        "labels": [v.name for v in venues],
        "values": [sum(b.total_price for e in v.events for b in e.bookings if b.status == "booked")
                   for v in venues],
    }
    total_revenue = sum(revenue_chart["values"])
    return render_template("admin/summary.html", seats_chart=seats_chart,
                           revenue_chart=revenue_chart, total_revenue=total_revenue)


# ---------- Search ----------

@admin_bp.route("/search")
@admin_required
def search():
    q = request.args.get("q", "").strip()
    kind = request.args.get("type", "events")
    results = []
    if q:
        like = f"%{q}%"
        if kind == "users":
            results = User.query.filter(User.name.ilike(like) | User.email.ilike(like)).all()
        elif kind == "venues":
            results = Venue.query.filter(Venue.name.ilike(like) | Venue.city.ilike(like)).all()
        else:
            kind = "events"
            results = Event.query.filter(Event.title.ilike(like)).order_by(Event.date_time).all()
    return render_template("admin/search.html", q=q, kind=kind, results=results)
