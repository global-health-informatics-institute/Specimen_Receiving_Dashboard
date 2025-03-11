from datetime import timedelta
import app
from extensions.extensions import db, logger, application_config, start_time
from models.test_definitions_model import Test_Definition
from models.tests_model import Test

# get all test ids
def get_type_id(key):
    """
    Retrieve the test type ID based on the provided key.
    """
    _test_type_ids = {
        "1": application_config["test_short_name"].get("test_type_1"),
        "2": application_config["test_short_name"].get("test_type_2"),
        "3": application_config["test_short_name"].get("test_type_3"),
        "4": application_config["test_short_name"].get("test_type_4"),
    }
    test_type_short_name = _test_type_ids.get(key)
    if not test_type_short_name:
        logger.error(f"No test short name found for key {key}")
        return None

    try:
        test_type = db.session.query(Test_Definition).filter(
            Test_Definition.test_short_name == test_type_short_name
        ).first()
        if not test_type:
            logger.error(f"No test definition found for short name {test_type_short_name}")
            return None
        return test_type.test_id
    except Exception as e:
        logger.error(f"Error getting ID for {test_type_short_name}: {e}")
        return None


# get count of todays tests based on the passed test_type_id
def get_test_count(test_type_id, status):
    """
    Retrieve the count of tests for the given test type ID.
    """
    try:
        test_count = db.session.query(Test).filter(
            Test.test_test_type == test_type_id,
            Test.test_test_status == status,
            (Test.created_at) >= start_time(),
        ).count()
        return test_count
    except Exception as e:
        logger.error(f"Error getting count for {test_type_id}: {e}")
        return None

def all_registered():
    return {
        "registered_test_type_1": get_test_count(get_type_id("1"), "1"),
        "registered_test_type_2": get_test_count(get_type_id("2"), "1"),
        "registered_test_type_3": get_test_count(get_type_id("3"), "1"),
        "registered_test_type_4": get_test_count(get_type_id("4"), "1"),
    }


def all_received():
    return {
        "received_test_type_1": get_test_count(get_type_id("1"), "2"),
        "received_test_type_2": get_test_count(get_type_id("2"), "2"),
        "received_test_type_3": get_test_count(get_type_id("3"), "2"),
        "received_test_type_4": get_test_count(get_type_id("4"), "2"),
    }


def all_in_progress():
    return {
        "in_progress_test_type_1": get_test_count(get_type_id("1"),"3"),
        "in_progress_test_type_2": get_test_count(get_type_id("2"),"3"),
        "in_progress_test_type_3": get_test_count(get_type_id("3"),"3"),
        "in_progress_test_type_4": get_test_count(get_type_id("4"),"3"),
    }


def all_pending_auth():
    return{
        "pending_auth_test_type_1": get_test_count(get_type_id("1"),"4"),
        "pending_auth_test_type_2": get_test_count(get_type_id("2"),"4"),
        "pending_auth_test_type_3": get_test_count(get_type_id("3"),"4"),
        "pending_auth_test_type_4": get_test_count(get_type_id("4"),"4"),
    }


def all_completed():
    return {
        "completed_test_type_1": get_test_count(get_type_id("1"),"5"),
        "completed_test_type_2": get_test_count(get_type_id("2"),"5"),
        "completed_test_type_3": get_test_count(get_type_id("3"),"5"),
        "completed_test_type_4": get_test_count(get_type_id("4"),"5"),
    }


def all_rejected():
    return {
        "rejected_test_type_1": get_test_count(get_type_id("1"),"6"),
        "rejected_test_type_2": get_test_count(get_type_id("2"),"6"),
        "rejected_test_type_3": get_test_count(get_type_id("3"),"6"),
        "rejected_test_type_4": get_test_count(get_type_id("4"),"6"),
    }

def all_test_counts():
    return {
        "registered": all_registered(),
        "received": all_received(),
        "in_progress": all_in_progress(),
        "pending_auth": all_pending_auth(),
        "completed": all_completed(),
        "rejected": all_rejected()
    }
    

# example usage:
# app = app.create_app()
# if __name__ == "__main__":
#     with app.app_context():
#         logger.info(get_type_id("1"))
#         logger.info(get_type_id("2"))
#         logger.info(get_type_id("3"))
#         logger.info(get_type_id("4"))
#         logger.info(get_test_count("40","1"))
#         logger.info(get_test_count("2","1"))
#         logger.info(get_test_count("3","1"))
#         logger.info(get_test_count("4","1"))
