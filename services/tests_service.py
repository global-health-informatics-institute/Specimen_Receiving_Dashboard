import app
from extensions.extensions import db, logger, application_config
from models.test_definitions_model import Test_Definition

# get all test ids
def all_test_type_ids(key):
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


# get todays tests based on the passed test_type_id
# test_state

app = app.create_app()
if __name__ == "__main__":
    with app.app_context():
        print(all_test_type_ids("1"))
        print(all_test_type_ids("2"))
        print(all_test_type_ids("3"))
        print(all_test_type_ids("4"))