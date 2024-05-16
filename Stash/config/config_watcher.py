import os
import json
import threading
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

script_dir = os.path.dirname(__file__)  # Absolute dir this script is in
rel_path = "department.config"
abs_file_path = os.path.join(script_dir, rel_path)

# Path to your department.config file
CONFIG_FILE_PATH = abs_file_path


# Function to load the department data
def load_department_data():
    data = {}
    try:
        with open(CONFIG_FILE_PATH, 'r') as json_file:
            data = json.load(json_file)
    except FileNotFoundError:
        data = {}
    return data


# Initial department data
department_data = load_department_data()


# Function to reload the department data
def reload_department_data():
    global department_data
    department_data = load_department_data()


# Watch for changes in the department.config file
class ConfigFileHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path == CONFIG_FILE_PATH:
            reload_department_data()


# Initialize the watchdog observer
observer = Observer()
event_handler = ConfigFileHandler()
observer.schedule(event_handler, path=os.path.dirname(CONFIG_FILE_PATH), recursive=False)
observer.start()


# function to periodically reload the configuration file
def reload_config_periodically(interval_seconds):
    while True:
        reload_department_data()
        time.sleep(interval_seconds)


reload_thread = threading.Thread(target=reload_config_periodically, args=(60,))
reload_thread.daemon = True
reload_thread.start()
