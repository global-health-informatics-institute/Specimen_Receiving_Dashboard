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

base_url = application_config["lims"]["base_url"]
api_version = application_config["lims"]["authentication"]["api_version"]
auth_url = base_url + api_version + application_config["lims"]["authentication"]["auth_endpoint"]
refresh_token_url = base_url + api_version + application_config["lims"]["authentication"]["refresh_token_endpoint"]

TEST_LIST_URL = base_url + api_version + application_config["lims"]["tests"]["test_list_endpoint"]
FETCH_START_DATE = datetime.now().strftime("%Y-%m-%d") 
FETCH_END_DATE = datetime.now().strftime("%Y-%m-%d")
DEPARTMENT_ID = application_config["department_id"]
LAB_LOCATION_ID = application_config["lab_location_id"]
MINIMAL = application_config["lims"]["tests"]["minimal"]

# apis services
STATUS_VOIDED = 0
STATUS_NEW = 1
