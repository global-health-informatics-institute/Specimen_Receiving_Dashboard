import logging
from app import create_app
from extensions.extensions import db, application_config
from models.monthly_count_model import Monthly_Count

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

department_id = application_config['department_id']

COLUMN_MAPPING = {
    1: "monthly_count_registered",
    2: "monthly_count_received",
    3: "monthly_count_progress",
    4: "monthly_count_pending",
    5: "monthly_count_complete",
    0: "monthly_count_rejected",
}


def _counter_value(action, column=None):
    """
    Handles fetching or updating monthly counter values.
    Args:
        action (str): "fetch", "increment", or "decrement".
        column (int, optional): The column identifier for updating or fetching.
    Returns:
        dict, int, or None: 
        - Returns all counters as a dictionary for "fetch" without a column.
        - Returns a specific counter value as an int for "fetch" with a column.
        - Returns None for update actions.
    """
    table = Monthly_Count
    column_name = COLUMN_MAPPING.get(column)

    try:
        if action == "fetch":
            count = db.session.query(table).filter_by(department_id=department_id).first()
            if count:
                if column_name:  # Fetch a specific column value
                    return getattr(count, column_name, 0)
                # Fetch all counter values
                return {col: getattr(count, col) for col in COLUMN_MAPPING.values()}
            logger.warning(f"No counters found for department_id {department_id}.")
            return {} if not column_name else 0

        if action in ["increment", "decrement"] and column_name:
            adjustment = 1 if action == "increment" else -1
            current_value = getattr(
                db.session.query(table).filter_by(department_id=department_id).first(), column_name, 0
            )
            if current_value is None or current_value + adjustment < 0:
                logger.warning(f"Cannot {action} {column_name} below 0 for department_id {department_id}.")
                return

            result = db.session.query(table).filter_by(department_id=department_id).update(
                {column_name: table.__table__.c[column_name] + adjustment},
                synchronize_session=False
            )
            db.session.commit()
            if result:
                logger.info(f"{action.capitalize()}ed {column_name} for department_id {department_id}.")
            else:
                logger.warning(f"No rows updated for department_id {department_id}.")
        else:
            logger.error("Invalid action or column specified.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error during {action}: {e}")


def get_counter_values(column_id=None):
    """
    Fetch counter values for the department.
    Args:
        column_id (int, optional): If provided, fetches the value of the specific column.
    Returns:
        dict or int: Returns all counters as a dictionary or a specific counter value as an int.
    """
    return _counter_value("fetch", column=column_id)

def update_counter(action, column_id):
    """Update a specific counter."""
    _counter_value(action, column_id)


if __name__ == "__main__":
    app = create_app()
    with app.app_context():


        # example usage
        # Fetch all counter values
        logger.info(get_counter_values())
        
        # Increment a specific counter
        update_counter("increment", 2)
        
        # Fetch a specific counter value
        monthly_count_received = get_counter_values(2)
        logger.info(f"Monthly Count Received: {monthly_count_received}")
