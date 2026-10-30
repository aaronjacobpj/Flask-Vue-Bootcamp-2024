"""EventHub - Day 2: HTML pages with Jinja2 templates and Bootstrap.

Run:  python app.py   then open http://127.0.0.1:5000
"""
from flask import Flask, render_template

app = Flask(__name__)

# Hard-coded data for today. On Day 3 this list is replaced by a database query.
EVENTS = [
    {"id": 1, "title": "Indie Music Night", "venue": "Blue Frog", "city": "Chennai",
     "date": "2026-11-07 19:00", "price": 499, "seats_left": 42},
    {"id": 2, "title": "Python Meetup", "venue": "IITM Research Park", "city": "Chennai",
     "date": "2026-11-12 18:30", "price": 0, "seats_left": 0},
    {"id": 3, "title": "Stand-up Comedy Special", "venue": "Phoenix Hall", "city": "Bengaluru",
     "date": "2026-11-20 20:00", "price": 799, "seats_left": 120},
]


@app.route("/")
def index():
    return render_template("index.html", events=EVENTS)


@app.route("/login")
def login():
    return render_template("auth/login.html")


@app.route("/register")
def register():
    return render_template("auth/register.html")


@app.route("/admin")
def admin_dashboard():
    return render_template("admin/dashboard.html", events=EVENTS)


if __name__ == "__main__":
    app.run(debug=True)
