from sqlalchemy import text
from extensions.extensions import db, logger, application_config
from models.test_definitions_model import Test_Definition
import app


department_id = application_config["department_id"]

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

def tat_average(test_type):
    """
    Calculate the average Turnaround Time (TAT) in minutes for the given test type.
    """
    try:
        test_type_id = all_test_type_ids(test_type)
        if not test_type_id:
            logger.error(f"Invalid test type provided: {test_type}")
            return None

        logger.info(f"Resolved test_type_id: {test_type_id}")

        query = text("""
            SELECT 
                IFNULL(ROUND(AVG(TIMESTAMPDIFF(MINUTE, created_at, updated_at)), 2), 0) AS average_duration_in_minutes
            FROM 
                tests
            WHERE 
                test_test_status = 5
                AND test_test_type = :test_type_id
                AND created_at >= (CURDATE() - INTERVAL (DAYOFWEEK(CURDATE()) - 2) DAY)
                AND created_at <= NOW();
        """)


        # Execute the query
        current_tat = db.session.execute(
            query,
            {"test_type_id": test_type_id}
        ).first()
        # Debug: Log the query result
        logger.info(f"Query result: {current_tat}")

        
        return current_tat[0] if current_tat else 0.0
    except Exception as e:
        logger.error(f"Failed to calculate TAT for test_type {test_type}: {e}")
        return 0

if __name__ == "__main__":
    app = app.create_app()
    with app.app_context():
        for test_type in ["1", "2", "3", "4"]:
            tat_result = tat_average(test_type)
            print(f"TAT for test type {test_type}: {tat_result}")
        print(type(tat_average("1"))) #pass index as key to access the test type shortname

