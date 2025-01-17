import yaml
"""
Return screen size css if using_orange_pi is False
"""
with open("config/application.config.yaml", "r") as file:
    application_config = yaml.safe_load(file)

def serve_static():
    static_data = {
        "screen" : application_config["using_orange_pi"],
        "department_name": application_config["department"]
    }
    return static_data