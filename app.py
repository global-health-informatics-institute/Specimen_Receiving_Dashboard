from flask import Flask
from extensions.extensions import db
from flask_migrate import Migrate
from models import status_definitions_model, department_model, oerr_status_model


def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    from extensions.extensions import dashboard_uri
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = dashboard_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Initialize the extensions
    db.init_app(app)

    # Set up Flask-Migrate
    Migrate(app, db)

    # Import and register Blueprints with prefixes
    from routes.dashboard_route import dashboard_bp

    # Register each Blueprint with its respective prefix
    app.register_blueprint(dashboard_bp)

    return app
