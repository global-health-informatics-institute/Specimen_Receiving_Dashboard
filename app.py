from flask import Flask
from extensions.extensions import db
from flask_migrate import Migrate

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
    # app.register_blueprint(fixed_bp,)
    # app.register_blueprint(index_bp,)
    # app.register_blueprint(office_bp,)
    # app.register_blueprint(office_management_bp,)
    # app.register_blueprint(order_management_bp,)
    # app.register_blueprint(order_bp,)
    # app.register_blueprint(pos_bp,)
    # app.register_blueprint(side_bp,)
    # app.register_blueprint(stock_bp,)
    # app.register_blueprint(login_bp,)
    # app.register_blueprint(warehouse_bp,)
    # app.register_blueprint(settings_bp,)

    return app
