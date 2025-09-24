from extensions.extensions import application_config

# Cache to store the result of serve_static
_cached_static_data = None

def serve_static():
    global _cached_static_data


    # If the data is already cached, return it
    if _cached_static_data is not None:
        return _cached_static_data
 
    # Compute the data only once
    if application_config["using_orange_pi"]:
        JS_BASE_URL = '/js/pi/'
        CSS_FILE = 'css/orange_pi.css'
    else:
        JS_BASE_URL = '/js/acer/'
        CSS_FILE = 'css/screen.css'

    department_name = application_config["department"]
    department_id = application_config["department_id"]

    test_type_1 = application_config["test_short_name"]["test_type_1"]
    test_type_2 = application_config["test_short_name"]["test_type_2"]
    test_type_3 = application_config["test_short_name"]["test_type_3"]
    test_type_4 = application_config["test_short_name"]["test_type_4"]


    
    # Cache the result
    _cached_static_data = {
        "JS_BASE_URL": JS_BASE_URL,
        "CSS_FILE": CSS_FILE,
        "department_name": department_name,
        "department_id": department_id,
        "test_type_1": test_type_1,
        "test_type_2": test_type_2,
        "test_type_3": test_type_3,
        "test_type_4": test_type_4,
    }

    return _cached_static_data
