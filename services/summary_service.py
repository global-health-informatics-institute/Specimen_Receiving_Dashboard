from datetime import datetime, timedelta
from app import create_app
from extensions.extensions import db, logger, application_config
from models.test_definitions_model import Test_Definition
from models.tests_model import Test


# Application configurations
days = application_config["days"]
hours = application_config["hours"]

start_time = datetime.now() - timedelta(days=days, hours=hours)

def _get_test_type_id(test_type):
    """
    Fetches the test type ID for a given test short name.
    """
    try:
        result = db.session.query(Test_Definition).filter(Test_Definition.test_short_name == test_type).first()
        if result:
            return result.test_id
        else:
            logger.warning(f"No matching short name found for {test_type}")
            return None
    except Exception as e:
        logger.error(f"Error fetching test type ID: {e}")
        return None

def _initialize_test_type_ids():
    """
    Initializes test type IDs by fetching them within the application context.
    """
    with app.app_context():
        return [
            _get_test_type_id(application_config["test_short_name"].get(f"test_type_{i}"))
            for i in range(1, 5)
        ]

# Create the Flask app
app = create_app()

# Initialize test type IDs
_test_type_ids = _initialize_test_type_ids()


def _count_tests(status, additional_statuses=None):
    """
    Count tests for specific statuses within the defined time constraints.
    """
    try:
        statuses = [status] + (additional_statuses or [])
        start_time 

        count = db.session.query(Test).filter(
            Test.test_test_type.in_(_test_type_ids),
            Test.test_test_status.in_(statuses),
            Test.created_at >= start_time,
        ).count()
        return count or 0
    except Exception as e:
        logger.error(f"Error counting tests for status {status}: {e}")
        return 0

# Status-specific count functions
def count_registered():
    return _count_tests("2")

def count_received():
    return _count_tests("0")

def count_in_progress():
    return _count_tests("3")

def count_pending_auth():
    return _count_tests("4")

def count_completed():
    return _count_tests("5")

def count_rejected():
    return _count_tests("6", additional_statuses=["7", "8", "9"])

# Test the counts
if __name__ == "__main__":
    with app.app_context():
        print(count_completed())
