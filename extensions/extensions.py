import mysql.connector
import logging
import yaml
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

with open("config/application.config.yml", "r") as file:
    config = yaml.safe_load(file)


with open('data/departments.yml', 'r') as file:
    department_data = yaml.safe_load(file)


with open('data/test_types.yml', 'r') as file:
    test_type_data = yaml.safe_load(file)

with open('data/lab_locations.yml', 'r') as file:
    lab_location_data = yaml.safe_load(file)


department_data = department_data
test_type_data = test_type_data
lab_location_data = lab_location_data


application_config = config 

dt = datetime
db = SQLAlchemy()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

application_config = config['application_config']
dashboard_uri = f'mysql+pymysql://{application_config["dashboard"]["user"]}:{application_config["dashboard"]["password"]}@{application_config["dashboard"]["host"]}/{application_config["dashboard"]["database"]}'


def start_time():
    from datetime import datetime, timedelta
    """
    Returns the most recent occurrence of 7:00 AM.
    """
    now = datetime.now()
    if now.hour >= 7:
        result = now.replace(hour=7, minute=0, second=0, microsecond=0)
    else: 
        result = (now - timedelta(days=1)).replace(hour=7, minute=0, second=0, microsecond=0)
    return result
