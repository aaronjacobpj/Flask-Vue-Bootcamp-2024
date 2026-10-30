"""Route guards. Put them *below* @blueprint.route(...)."""
from functools import wraps

from flask import abort, flash, redirect, url_for
from flask_login import current_user, login_required


def admin_required(view):
    """Only a logged-in admin may open this page. Others get 403 Forbidden."""
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return view(*args, **kwargs)
    return wrapper


def user_required(view):
    """Only a logged-in normal user (not the admin) may do this, e.g. book seats."""
    @wraps(view)
    @login_required
    def wrapper(*args, **kwargs):
        if current_user.is_admin:
            flash("The admin account cannot book events. Log in as a user.", "warning")
            return redirect(url_for("admin.dashboard"))
        return view(*args, **kwargs)
    return wrapper
