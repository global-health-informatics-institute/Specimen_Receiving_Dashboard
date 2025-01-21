from extensions.extensions import application_config
"""
Return screen size css if using_orange_pi is False
"""

def serve_static():
    if application_config["using_orange_pi"]:
        JS_BASE_URL = '/js/pi/'
        CSS_FILE = 'css/orange_pi.css'
    else:
        JS_BASE_URL = '/js/acer/'
        CSS_FILE = 'css/screen.css'
    department_name = application_config["department"]
    return {
        "JS_BASE_URL": JS_BASE_URL,
        "CSS_FILE": CSS_FILE,
        "department_name": department_name
    }