import json
from flask import Flask
from apis.tat_api import  tat_bp
from apis.monthly_summary_api import monthly_summary_bp
from apis.weekly_summary_api import weekly_summary_bp 
from apis.test_type_bp import test_type_bp
from apis.test_type_reference import(TEST_TYPE_REFERENCE)
from config.application import application_config

def map_types_to_id():
    test_short_name1 = application_config["test_short_name"]["test_type_1"]
    test_short_name2 = application_config["test_short_name"]["test_type_2"]
    test_short_name3 = application_config["test_short_name"]["test_type_3"]
    test_short_name4 = application_config["test_short_name"]["test_type_4"]

    TEST_TYPE1 = TEST_TYPE_REFERENCE.get(f"{test_short_name1}")
test_types = map_types_to_id()


app = Flask(__name__)

app.register_blueprint(tat_bp,)
app.register_blueprint(weekly_summary_bp)
app.register_blueprint(monthly_summary_bp)
app.register_blueprint(test_type_bp)
app.register_blueprint(ward_bp)
app.register_blueprint(specimen_bp)
app.register_blueprint(department_bp)
app.register_blueprint(oerr_bp)


settings = {}
with open(config_file) as json_file:
    settings = json.load(json_file)


if __name__ == "__main__":
    
    connect_to_tokken()
    connect_to_test_types()
    connect_to_test_panels()
    connect_to_oerr_test()
    TOKEN = load_token_from_db() 
    app_port = settings.get("app", {}).get("port", 8001)
    app.run(host="0.0.0.0", port=app_port, debug=True)
