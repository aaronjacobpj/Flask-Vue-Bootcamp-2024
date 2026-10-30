"""EventHub - final version (Day 9): a Flask + SQLite event-booking app.

Run:  python app.py   then open http://127.0.0.1:5000
Admin login: admin@eventhub.com / admin123
"""
from flask import Flask, render_template
from flask_login import LoginManager

from config import Config
from models import User, db
from seed import create_admin

login_manager = LoginManager()
login_manager.login_view = "auth.login"  # where @login_required sends logged-out visitors
login_manager.login_message_category = "warning"


@login_manager.user_loader
def load_user(user_id):
    """Flask-Login calls this on every request to turn the id in the session into a User."""
    user = db.session.get(User, int(user_id))
    if user is None or user.is_flagged:
        return None  # a flagged user is logged out on their next request
    return user


def create_app(config_class=Config):
    """App factory: build and configure the Flask app in one place."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    login_manager.init_app(app)

    from routes.admin import admin_bp
    from routes.auth import auth_bp
    from routes.user import user_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    from api import api_bp
    app.register_blueprint(api_bp)

    @app.errorhandler(403)
    def forbidden(error):
        return render_template("error.html", code=403, message="You are not allowed to open this page."), 403

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", code=404, message="Page not found."), 404

    with app.app_context():
        db.create_all()
        create_admin(app)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
