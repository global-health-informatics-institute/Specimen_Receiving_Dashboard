from config.application import application_config

def serve_static():
    static_data = {
        "screen" : application_config["using_orange_pi"],
        "department_name": application_config["department"]
    }
    return static_data