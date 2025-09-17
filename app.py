from flask import Flask
from flask_migrate import Migrate
from extensions.extensions import dashboard_uri, db
from models import (
    authtoken_model, department_model, lab_location_model, monthly_count_model,
    oerr_status_model, status_definitions_model, test_definitions_model, tests_model,
    weekly_count_model
)


app = Flask(__name__)



app.config['SQLALCHEMY_DATABASE_URI'] = dashboard_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True

db.init_app(app)
Migrate(app, db)



settings = {}

if __name__ == "__main__":
    app_port = settings.get("app", {}).get("port", 8001)
    app.run(host="0.0.0.0", port=app_port, debug=True)
