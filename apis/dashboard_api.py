from flask import Flask
from apis.load_entries import load_entries_bp
from extensions.extensions import dashboard_uri, db


app = Flask(__name__)

app.register_blueprint(load_entries_bp)
app.register_blueprint(remove_entries_bp)


app.config['SQLALCHEMY_DATABASE_URI'] = dashboard_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db.init_app(app)



settings = {}

if __name__ == "__main__":
    app_port = settings.get("app", {}).get("port", 8001)
    app.run(host="0.0.0.0", port=app_port, debug=True)
