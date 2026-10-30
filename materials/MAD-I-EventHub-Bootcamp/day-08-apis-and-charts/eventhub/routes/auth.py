"""Register, login and logout using Flask-Login."""
from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from models import User, db

auth_bp = Blueprint("auth", __name__)


def home_for(user):
    """Where each role lands after login."""
    return url_for("admin.dashboard") if user.is_admin else url_for("user.index")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(home_for(current_user))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        confirm = request.form.get("confirm", "")

        # Always validate on the server too: HTML `required` can be bypassed easily.
        errors = []
        if not name or not email or not password:
            errors.append("All fields are required.")
        if email and "@" not in email:
            errors.append("Enter a valid email address.")
        if len(password) < 6:
            errors.append("Password must be at least 6 characters.")
        if password != confirm:
            errors.append("Passwords do not match.")
        if email and User.query.filter_by(email=email).first():
            errors.append("An account with this email already exists.")

        if errors:
            for error in errors:
                flash(error, "danger")
        else:
            user = User(name=name, email=email, role="user")  # sign-up can never create an admin
            user.set_password(password)
            db.session.add(user)
            db.session.commit()
            flash("Account created. Please log in.", "success")
            return redirect(url_for("auth.login"))

    return render_template("auth/register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(home_for(current_user))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user = User.query.filter_by(email=email).first()

        # Same message for "no such email" and "wrong password": do not reveal which emails exist.
        if user is None or not user.check_password(password):
            flash("Wrong email or password.", "danger")
        elif user.is_flagged:
            flash("Your account has been flagged by the admin.", "danger")
        else:
            login_user(user)  # stores the user's id in the signed session cookie
            flash(f"Welcome, {user.name}!", "success")
            return redirect(home_for(user))

    return render_template("auth/login.html")


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))
