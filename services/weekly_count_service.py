import logging
from app import create_app
from extensions.extensions import db, application_config
from models.weekly_count_model import Weekly_Count

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

department_id = application_config["department_id"]

# Helper function
def _counter_value(action, column=None):
    """
    Handles fetching or updating weekly counter values.
    Args:
        action (str): "fetch" to get counter values, "increment" to increase, or "decrement" to decrease a column.
        column (int, optional): The column identifier for updating. Not required for fetching all.
    Returns:
        dict or int: Returns fetched values as a dictionary or 0 in case of an error.
    """
    table = Weekly_Count
    column_mapping = {
        2: table.weekly_count_registered,
        0: table.weekly_count_received,
        3: table.weekly_count_progress,
        4: table.weekly_count_pending,
        5: table.weekly_count_complete,
        6: table.weekly_count_rejected,
        7: table.weekly_count_rejected,
        8: table.weekly_count_rejected,
        9: table.weekly_count_rejected,
    }
    column_name = column_mapping.get(column)

    try:
        if action == "fetch":
            # Fetch all counter values for the department
            count = db.session.query(table).filter(
                table.department_id == department_id
            ).first()
            if count:
                return {
                    "registered": count.weekly_count_registered,
                    "received": count.weekly_count_received,
                    "in_progress": count.weekly_count_progress,
                    "pending_auth": count.weekly_count_pending,
                    "complete": count.weekly_count_complete,
                    "rejected": count.weekly_count_rejected,
                }
            else:
                logger.warning(f"No counts found for department_id {department_id}.")
                return {}

        elif action in ["increment", "decrement"] and column_name:
            # Determine adjustment value based on action
            adjustment = 1 if action == "increment" else -1
            
            # If decrementing, ensure the value doesn't go below zero
            if action == "decrement":
                current_value = db.session.query(column_name).filter_by(department_id=department_id).scalar()
                if current_value is not None and current_value <= 0:
                    logger.warning(f"Cannot decrement {column_name}. Value already at 0 for department_id {department_id}.")
                    return

            # Update the specified column value
            result = db.session.query(table).filter_by(department_id=department_id).update(
                {column_name: column_name + adjustment},
                synchronize_session="fetch"
            )
            db.session.commit()

            if result:
                logger.info(f"Successfully {action}ed {column_name} for department_id {department_id}")
            else:
                logger.warning(f"No rows updated in {table.__tablename__} for department_id {department_id}")
        else:
            logger.error("Invalid action or column specified.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during {action}: {e}")
        return 0

# fetch
def get_counter_values():
    return _counter_value("fetch")


# increment
def increment_registered():
    _counter_value("increment", 2)

def increment_received():
    _counter_value("increment", 0)

def increment_in_progress():
    _counter_value("increment", 3)

def increment_pending_auth():
    _counter_value("increment", 4)

def increment_complete():
    _counter_value("increment", 5)

def increment_rejected():
    _counter_value("increment", 9)


# decrement
def decrement_registered():
    _counter_value("decrement", 2)

def decrement_received():
    _counter_value("decrement", 0)

def decrement_in_progress():
    _counter_value("decrement", 3)

def decrement_pending_auth():
    _counter_value("decrement", 4)

def decrement_complete():
    _counter_value("decrement", 5)

def decrement_rejected():
    _counter_value("decrement", 9)


if __name__ == "__main__":
    app = create_app()

    with app.app_context():
        ""