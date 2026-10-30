import os

from flask import Flask, jsonify
from flask_cors import CORS
from flask_security import SQLAlchemyUserDatastore

from config import Config
from application.extensions import db, security, cache
from application.models import User, Role
from application.seed import seed_database
from application.celery_app import celery_init_app


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    os.makedirs(os.path.join(app.root_path, "instance"), exist_ok=True)

    # --- extensions ---
    db.init_app(app)
    cache.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore, register_blueprint=False)
    # Allow the Vue dev server (different origin) to call /api/*
    CORS(app, resources={r"/api/*": {"origins": app.config["FRONTEND_ORIGIN"]}},
         allow_headers=["Content-Type", "Authentication-Token"])

    # Always answer auth failures with JSON (not HTML redirects)
    @security.unauthn_handler
    def unauthenticated(mechanisms=None, headers=None):
        return jsonify(message="Authentication required. Please log in."), 401

    @security.unauthz_handler
    def unauthorized(func_name=None, params=None):
        return jsonify(message="You are not allowed to access this resource."), 403

    # --- Celery (background jobs) ---
    celery_init_app(app)

    # --- blueprints ---
    from application.api.auth import auth_bp
    from application.api.resources import resources_bp
    from application.api.user import user_bp
    from application.api.admin import admin_bp
    from application.api.jobs import jobs_bp
    from application.api.summary import summary_bp
    for bp in (auth_bp, resources_bp, user_bp, admin_bp, jobs_bp, summary_bp):
        app.register_blueprint(bp)

    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    @app.errorhandler(404)
    def not_found(e):
        return jsonify(message="Not found"), 404

    with app.app_context():
        seed_database()
        cache.clear()  # start every run with an empty cache (avoids stale data after a DB reset)

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
