"""Login and registration pages. They only display forms today; Day 6 makes them work."""
from flask import Blueprint, render_template

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login")
def login():
    return render_template("auth/login.html")


@auth_bp.route("/register")
def register():
    return render_template("auth/register.html")
