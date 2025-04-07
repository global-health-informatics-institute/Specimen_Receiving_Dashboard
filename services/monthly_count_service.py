import logging
from app import create_app
from extensions.extensions import db, application_config, logger
from models.monthly_count_model import Monthly_Count

# Set up department ID and column mappings
department_id = application_config["department_id"]

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
        column (int, optional): Column identifier for updating. Not required for fetching all.
    Returns:
        dict or None: Counter values as a dictionary for "fetch", None for update actions.
    """
    table = Monthly_Count
    column_name = COLUMN_MAPPING.get(column)

    try:
        if action == "fetch":
            count = db.session.query(table).filter_by(department_id=department_id).first()
            if count:
                return {col: getattr(count, col) for col in COLUMN_MAPPING.values()}
            logger.warning(f"No counts found for department_id {department_id}.")
            return {}

        if action in ["increment", "decrement"] and column_name:
            adjustment = 1 if action == "increment" else -1
            current_value = getattr(
                db.session.query(table).filter_by(department_id=department_id).first(),
                column_name,
                0
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


def update_counter(action, column_id):
    """Update a specific counter."""
    _counter_value(action, column_id)


def get_monthly_counter_values():
    """Fetch all counters for the department."""
    return _counter_value("fetch")


def log_specific_counter(column_id):
    """Log a specific counter value."""
    column_name = COLUMN_MAPPING.get(column_id)
    if column_name:
        values = get_monthly_counter_values()
        if values:
            logger.info(f"{column_name}: {values.get(column_name)}")
    else:
        logger.error(f"Invalid column_id: {column_id}")


# Increment/Decrement helpers
def monthly_increment(column_id):
    update_counter("increment", column_id)


def monthly_decrement(column_id):
    update_counter("decrement", column_id)


def all_monthly_counts():
    """Fetch all monthly counts."""
    return db.session.query(Monthly_Count).all()
if __name__ == "__main__":
    app = create_app()

    # with app.app_context():
    #     # Example usage
    #     logger.info(get_monthly_counter_values())  # Log all values
        # increment(2)  # Increment registered
        # decrement(0)  # Increment received
        # log_specific_counter(0)  # Log monthly_count_received
        # logger.info(get_counter_values())  # Log updated values