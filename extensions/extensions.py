from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from config.application import application_config

dt = datetime
db = SQLAlchemy()

dashboard_uri = f'mysql+pymysql://{application_config["dashboard"]["user"]}:{application_config["dashboard"]["password"]}@{application_config["dashboard"]["host"]}/{application_config["dashboard"]["database"]}'

iblis_uri = f'mysql+pymysql://{application_config["iblis"]["user"]}:{application_config["iblis"]["password"]}@{application_config["iblis"]["host"]}:{application_config["iblis"]["port"]}/{application_config["iblis"]["database"]}'
