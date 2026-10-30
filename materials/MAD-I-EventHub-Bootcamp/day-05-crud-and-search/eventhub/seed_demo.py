"""Optional demo data: 2 users, 3 venues, 6 events, a few bookings.

Run once:  python seed_demo.py
Logins:    admin@eventhub.com / admin123   (created by the app itself)
           priya@example.com  / user123
           rahul@example.com  / user123
"""
from datetime import datetime, timedelta

from app import create_app
from models import Booking, Event, User, Venue, db

app = create_app()

with app.app_context():
    if Venue.query.first():
        print("Demo data already exists. Delete instance/eventhub.db to start fresh.")
        raise SystemExit

    priya = User(name="Priya Sharma", email="priya@example.com")
    priya.set_password("user123")
    rahul = User(name="Rahul Nair", email="rahul@example.com")
    rahul.set_password("user123")

    blue_frog = Venue(name="Blue Frog", city="Chennai", address="Anna Salai", capacity=150)
    research_park = Venue(name="IITM Research Park", city="Chennai", address="Taramani", capacity=300)
    phoenix = Venue(name="Phoenix Hall", city="Bengaluru", address="Whitefield", capacity=500)

    now = datetime.now()

    def on(days_from_now, hour):
        """A date `days_from_now` days away (negative = past), at `hour`:00."""
        return (now + timedelta(days=days_from_now)).replace(hour=hour, minute=0, second=0, microsecond=0)

    events = [
        Event(title="Indie Music Night", venue=blue_frog, date_time=on(10, 19),
              price=499, total_seats=120, description="Three local bands, one long night."),
        Event(title="Jazz Brunch", venue=blue_frog, date_time=on(24, 11),
              price=899, total_seats=60, description="Live jazz with brunch."),
        Event(title="Python Meetup", venue=research_park, date_time=on(5, 18),
              price=0, total_seats=200, description="Talks on Flask, testing and packaging."),
        Event(title="Startup Pitch Day", venue=research_park, date_time=on(40, 10),
              price=199, total_seats=250, description="Ten startups, five minutes each."),
        Event(title="Stand-up Comedy Special", venue=phoenix, date_time=on(15, 20),
              price=799, total_seats=400, description="Two hours of stand-up."),
        Event(title="Last Month's Quiz Night", venue=phoenix, date_time=on(-20, 19),
              price=99, total_seats=100, description="A past event, to test history and charts."),
    ]

    bookings = [
        Booking(user=priya, event=events[0], seats=4),
        Booking(user=priya, event=events[2], seats=25),  # a group booking for a study circle
        Booking(user=priya, event=events[5], seats=3, booked_at=on(-30, 12)),
        Booking(user=rahul, event=events[0], seats=30),
        Booking(user=rahul, event=events[4], seats=50),
        Booking(user=rahul, event=events[3], seats=10),
        Booking(user=rahul, event=events[5], seats=2, booked_at=on(-25, 9)),
        Booking(user=rahul, event=events[1], seats=2, status="cancelled"),
    ]

    db.session.add_all([priya, rahul, blue_frog, research_park, phoenix, *events, *bookings])
    db.session.commit()
    print("Demo data added.")
