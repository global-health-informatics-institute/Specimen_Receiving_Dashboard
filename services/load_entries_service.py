import logging
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from app import create_app
from config.application import application_config
from extensions.extensions import iblis_uri, db
from models.monthly_count_model import Monthly_Count
from models.test_definitions_model import Test_Definition
from models.tests_model import Test
from models.weekly_count_model import Weekly_Count

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def get_test_type_id(test_type):
    try:
        result = db.session.query(Test_Definition).filter(Test_Definition.test_short_name == test_type).first()
        if result:
            return result.test_id
        else:
            logger.warning(f"No matching short name {test_type}")
            return None
    except Exception as e:
        logger.error(f"Error fetching test type ID: {e}")
        return None


# Define constants
interval = application_config["interval"]
timeout = application_config["refresh_rate"]
department_id = application_config["department_id"]

# Create session factories
iblis_engine = create_engine(iblis_uri)
iblis_session_maker = sessionmaker(bind=iblis_engine)

# Helper functions for updating weekly and monthly summaries
def _update_summary(session, table, status, department_id):
    """Helper to update weekly or monthly counters."""
    # Determine the correct column names based on the table
    if table == Weekly_Count:
        column_mapping = {
            2: table.weekly_count_registered,
            0: table.weekly_count_received,
            3: table.weekly_count_progress,
            4: table.weekly_count_pending,
            5: table.weekly_count_complete,
        }

    elif table == Monthly_Count:
        column_mapping = {
            2: table.monthly_count_registered,
            0: table.monthly_count_received,
            3: table.monthly_count_progress,
            4: table.monthly_count_pending,
            5: table.monthly_count_complete,
        }
    else:
        logger.error(f"Unsupported table: {table}")
        return

    # Get the correct column for the given status
    column_name = column_mapping.get(status)
    if not column_name:
        logger.warning(f"Unknown status: {status}")
        return

    # values being updated
    logger.info(f"Updating {table.__tablename__}, column {column_name}, for department_id {department_id}")

    # Perform the update
    result = session.query(table).filter_by(department_id=department_id).update(
        {column_name: column_name + 1},
        synchronize_session="fetch"
    )

    # succeeds or fails
    if result:
        logger.info(f"Successfully incremented {column_name} for department_id {department_id}")
    else:
        logger.warning(f"No rows updated in {table.__tablename__} for department_id {department_id}")



def load_entries():
    _test_type_ids = [
        get_test_type_id(application_config["test_short_name"]["test_type_1"]),
        get_test_type_id(application_config["test_short_name"]["test_type_2"]),
        get_test_type_id(application_config["test_short_name"]["test_type_3"]),
        get_test_type_id(application_config["test_short_name"]["test_type_4"]),
    ]
    _test_type_ids = [t for t in _test_type_ids if t is not None]  # Remove None values

    if not _test_type_ids:
        logger.error("No valid test type IDs found. Skipping load_entries execution.")
        return  # Exit early to avoid running the query with invalid parameters

    iblis_session = iblis_session_maker()
    try:
        # Use a raw SQL query to fetch the latest tests
        tests_query = text("""
            WITH RankedTests AS (
                SELECT 
                    specimens.accession_number AS accession_id,
                    tests.test_type_id AS test_type,
                    tests.test_status_id AS test_status,
                    ROW_NUMBER() OVER (
                        PARTITION BY specimens.accession_number, tests.test_type_id
                        ORDER BY tests.time_created DESC
                    ) AS rn
                FROM 
                    specimens
                INNER JOIN 
                    tests ON specimens.id = tests.specimen_id
                WHERE
                    specimens.time_accepted IS NOT NULL
                    AND specimens.specimen_type_id = :department_id
                    AND tests.test_status_id NOT IN (1, 6, 7, 8)
                    AND tests.time_created >= CURDATE() + INTERVAL :timeout HOUR
                    AND tests.time_created <= CURDATE() + INTERVAL :interval DAY + INTERVAL :timeout HOUR
                    AND tests.test_type_id IN :test_type_ids
            )
            SELECT
                accession_id,
                test_type,
                test_status
            FROM
                RankedTests
            WHERE
                rn = 1;
        """)

        # Execute the query and fetch results
        latest_tests = iblis_session.execute(
            tests_query,
            {
                "department_id": department_id,
                "timeout": timeout,
                "interval": interval,
                "test_type_ids": tuple(_test_type_ids),  # tuple for SQL compatibility
            }
        ).fetchall()

        # Process each result and update srsDB
        for test in latest_tests:
            accession_id, test_type, test_status = test[0], test[1], test[2]
            test_status_str = str(test_status)

            # if already exists in srsDB
            existing_test = (
                db.session.query(Test)
                .filter(Test.test_accession_id == accession_id, Test.test_test_type == test_type)
                .first()
            )

            if not existing_test:
                # Insert new record if not found
                new_test = Test(
                    test_accession_id=accession_id,
                    test_test_type=test_type,
                    test_test_status=test_status_str,
                )
                db.session.add(new_test)
                _update_summary(db.session, Weekly_Count, test_status, department_id)
                _update_summary(db.session, Monthly_Count, test_status, department_id)
                logger.info(f"Condition 1: Inserted new record for accession_id: {accession_id}, test_type: {test_type}, test_status: {test_status}")
            else:
                existing_status = int(existing_test.test_test_status)
                # Skip if the status hasn't changed
                if existing_status == test_status:
                    logger.info(f"Skipping update for accession_id: {accession_id}, test_type: {test_type}, test_status unchanged: {test_status}")
                    continue

                # Update logic if statuses are different
                existing_test.test_test_status = test_status_str
                _update_summary(db.session, Weekly_Count, test_status, department_id)
                _update_summary(db.session, Monthly_Count, test_status, department_id)

        # Commit the changes to srsDB
        db.session.commit()

    except SQLAlchemyError as e:
        logger.error(f"Error: {e}")
    finally:
        iblis_session.close()

if __name__ == "__main__":
    app = create_app()

    # Push the application context
    with app.app_context():
        load_entries()
