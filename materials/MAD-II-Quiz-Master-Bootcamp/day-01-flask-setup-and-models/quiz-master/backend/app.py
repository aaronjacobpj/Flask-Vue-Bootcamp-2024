import os

from flask import Flask, jsonify
from flask_security import SQLAlchemyUserDatastore

from config import Config
from application.extensions import db, security
from application.models import User, Role
from application.seed import seed_database


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # --- extensions ---
    db.init_app(app)
    datastore = SQLAlchemyUserDatastore(db, User, Role)
    security.init_app(app, datastore, register_blueprint=False)


    @app.get("/api/health")
    def health():
        return jsonify(status="ok")

    with app.app_context():
        seed_database()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
