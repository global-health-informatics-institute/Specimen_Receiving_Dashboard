import logging
import yaml
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

with open("config/application.config.yaml", "r") as file:
    config = yaml.safe_load(file)


application_config = config 

dt = datetime
db = SQLAlchemy()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


dashboard_uri = f'mysql+pymysql://{application_config["dashboard"]["user"]}:{application_config["dashboard"]["password"]}@{application_config["dashboard"]["host"]}/{application_config["dashboard"]["database"]}'

iblis_uri = f'mysql+pymysql://{application_config["iblis"]["user"]}:{application_config["iblis"]["password"]}@{application_config["iblis"]["host"]}:{application_config["iblis"]["port"]}/{application_config["iblis"]["database"]}'
