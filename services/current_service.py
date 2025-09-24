from sqlalchemy import text
from extensions.extensions import db, logger, application_config
from models.test_definitions_model import Test_Definition
import app


days = application_config["days"]
hours = application_config["clear_time"]
department_id = application_config["department_id"]



def all_test_type_ids(key):    
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

def tat_current(test_type):
    try:
        test_type_id = all_test_type_ids(test_type)
        if not test_type_id:
            logger.error(f"Invalid test type provided: {test_type}")
            return None

        query = text("""
            SELECT 
                IFNULL(ROUND(AVG(TIMESTAMPDIFF(MINUTE, created_at, updated_at)), 2), 0) AS average_duration_in_hours
            FROM 
                tests
            WHERE 
                created_at IS NOT NULL 
                AND test_test_status IS NOT NULL
                AND tests.test_test_status = 5
                AND tests.created_at >= CURDATE() + INTERVAL :hours HOUR
                AND tests.created_at <= CURDATE() + INTERVAL :days DAY + INTERVAL :hours HOUR 
                AND test_test_type = :test_type_id;
        """)

        current_tat = db.session.execute(
            query,
            {
                "hours": hours,
                "days": days,
                "test_type_id": test_type_id,
            }
        ).first()
        
        return current_tat[0] if current_tat else None
    except Exception as e:
        logger.error(f"Failed to get current TAT for {test_type}: {e}")
        return None
    
def all_current():
    return {
        "test_type_1": tat_current('1'),
        "test_type_2": tat_current('2'),
        "test_type_3": tat_current('3'),
        "test_type_4": tat_current('4'),
    }

# example usage
# app = app.create_app()
# if __name__ == "__main__":
#     with app.app_context():
#         print((tat_current("1"))) #pass index as key to access the test type shortname