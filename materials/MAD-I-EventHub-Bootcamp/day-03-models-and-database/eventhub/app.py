"""EventHub - Day 3: data comes from a SQLite database.

Run:  python app.py   then open http://127.0.0.1:5000
      (optional, once) python seed_demo.py   to add demo venues and events
"""
from datetime import datetime

from flask import Flask, render_template

from config import Config
from models import Event, Venue, db
from seed import create_admin


def create_app(config_class=Config):
    """App factory: build and configure the Flask app in one place."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    @app.route("/")
    def index():
        events = (Event.query.filter(Event.date_time >= datetime.now())
                  .order_by(Event.date_time).all())
        return render_template("index.html", events=events)

    @app.route("/login")
    def login():
        return render_template("auth/login.html")

    @app.route("/register")
    def register():
        return render_template("auth/register.html")

    @app.route("/admin")
    def admin_dashboard():
        venues = Venue.query.order_by(Venue.name).all()
        return render_template("admin/dashboard.html", venues=venues)

    # The database and its tables are created by code, never by hand.
    with app.app_context():
        db.create_all()
        create_admin(app)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
