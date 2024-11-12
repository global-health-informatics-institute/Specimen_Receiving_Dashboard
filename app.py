from flask import Flask
from flask_migrate import Migrate
from extensions.extensions import db, bcrypt

def create_app():
    app = Flask(__name__, template_folder="templates", static_folder="static")
    from config.application import uri
    # Database configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

    # Initialize the extensions
    db.init_app(app)

    # Set up Flask-Migrate
    Migrate(app, db)

    # # Import and register Blueprints with prefixes
    # from routes.catalog_route import catalog_bp
    # from routes.fixed_route import fixed_bp
    # from routes.index_route import index_bp
    # from routes.office_management_route import office_management_bp
    # from routes.office_route import office_bp
    # from routes.order_management_route import order_management_bp
    # from routes.order_route import order_bp
    # from routes.pos_route import pos_bp
    # from routes.side_route import side_bp
    # from routes.stock_route import stock_bp
    # from routes.login_route import login_bp
    # from routes.warehouse_route import warehouse_bp
    # from routes.settings_route import settings_bp

    # Register each Blueprint with its respective prefix
    # app.register_blueprint(catalog_bp,)
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
