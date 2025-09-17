from datetime import datetime, time, timedelta
from extensions.extensions import db, logger, application_config
from models.test_definitions_model import Test_Definition
from models.tests_model import Test


ACTIVE_DAYS_COUNT = application_config.get("active_count_days", 1)
ACTIVE_DAYS_START_TIME = application_config.get("active_count_day_start_time", 7)


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
    try:
        return [
            _get_test_type_id(application_config["test_short_name"].get(f"test_type_{i}"))
            for i in range(1, 5)
        ]
    except Exception as e:
        logger.error(f"Error initializing test type IDs: {e}")
        return []


def _count_tests(status):
    """
    Count tests for specific statuses within the defined time constraints.
    Uses ACTIVE_DAYS_COUNT and ACTIVE_DAYS_START_TIME from config.
    """
    _test_type_ids = _initialize_test_type_ids()

    try:
        if not _test_type_ids:
            logger.warning("No valid test type IDs initialized.")
            return 0

        # Calculate cutoff datetime
        today = datetime.now().date()
        start_date = today - timedelta(days=ACTIVE_DAYS_COUNT - 1)
        cutoff_datetime = datetime.combine(start_date, time(ACTIVE_DAYS_START_TIME, 0))
        count = db.session.query(Test).filter(
            Test.test_test_type.in_(_test_type_ids),
            Test.test_test_status == status,
            Test.created_at >= cutoff_datetime
        ).count()
        return count or 0
    except Exception as e:
        logger.error(f"Error counting tests for status {status}: {e}")
        return 0

# Status-specific count functions
def count_registered():
    return _count_tests("1")

def count_received():
    return _count_tests("2")

def count_in_progress():
    return _count_tests("3")

def count_pending_auth():
    return _count_tests("4")

def count_completed():
    return _count_tests("5")

def count_rejected():
    return _count_tests("0")

def all_summary_counts():
    return {
        "registered": (
            count_registered() +
            count_received() +
            count_in_progress() +
            count_pending_auth() +
            count_completed() +
            count_rejected()
        ),
        "received": count_received(),
        "in_progress": count_in_progress(),
        "pending_auth": count_pending_auth(),
        "completed": count_completed(),
        "rejected": count_rejected(),
    }
