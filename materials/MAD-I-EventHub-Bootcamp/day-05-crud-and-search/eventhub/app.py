"""EventHub - Day 5: routes split into blueprints; admin CRUD and search.

Run:  python app.py   then open http://127.0.0.1:5000
"""
from flask import Flask, render_template

from config import Config
from models import db
from seed import create_admin


def create_app(config_class=Config):
    """App factory: build and configure the Flask app in one place."""
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)

    # Blueprints keep related routes together in their own files.
    from routes.admin import admin_bp
    from routes.auth import auth_bp
    from routes.user import user_bp

    app.register_blueprint(user_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)

    @app.errorhandler(404)
    def not_found(error):
        return render_template("error.html", code=404, message="Page not found."), 404

    with app.app_context():
        db.create_all()
        create_admin(app)

    return app


if __name__ == "__main__":
    create_app().run(debug=True)
