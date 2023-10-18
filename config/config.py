import json
import os

data = {}


def load_department_data():
    global data
    try:
        script_dir = os.path.dirname(__file__)  # Absolute dir this script is in
        rel_path = "department.config"
        abs_file_path = os.path.join(script_dir, rel_path)
        with open(abs_file_path, 'r') as json_file:
            data = json.load(json_file)

    except FileNotFoundError:
        data = {}


def initialize_department_data():
    global data
    if not data:
        load_department_data()
    return data

