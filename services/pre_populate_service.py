"""
During set up, run the migration script and pre populate dependent attributes as python -m services.pre_populate_service
"""
from app import create_app
from sqlalchemy import create_engine, text
from extensions.extensions import db, iblis_uri,application_config
from models.monthly_count_model import Monthly_Count
from models.status_definitions_model import Test_Status_Definition
from sqlalchemy.orm import sessionmaker
from models.department_model import Department
import logging

from models.test_definitions_model import Test_Definition
from models.weekly_count_model import Weekly_Count

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# set up iblis session
iblis_engine = create_engine(iblis_uri)
iblis_session_maker = sessionmaker(bind=iblis_engine)    
iblis_session = iblis_session_maker()

# test types
test_types = [application_config["test_short_name"]["test_type_1"], application_config["test_short_name"]["test_type_2"], application_config["test_short_name"]["test_type_3"], application_config["test_short_name"]["test_type_4"]]
department_id = application_config["department_id"] #referenced as test_types.test_category_id 
department = application_config["department"]


def populate_status_definitions():
    try:
        # Check if the table is empty
        count = Test_Status_Definition.query.count()

        if count == 0:
            # Populate the status_definitions table
            status_definitions = [
                Test_Status_Definition(status_id=1, status_meaning="registered", test_status_id=2, test_status_meaning="Pending", specimen_status_id=2, specimen_status_meaning="specimen_accepted"),
                Test_Status_Definition(status_id=2, status_meaning="Received", test_status_id=3, test_status_meaning="Started", specimen_status_id=2, specimen_status_meaning="specimen_accepted"),
                Test_Status_Definition(status_id=3, status_meaning="inProgress", test_status_id=3, test_status_meaning="Started", specimen_status_id=2, specimen_status_meaning="specimen_accepted"),
                Test_Status_Definition(status_id=4, status_meaning="pendingAuth", test_status_id=4, test_status_meaning="Completed", specimen_status_id=2, specimen_status_meaning="specimen_accepted"),
                Test_Status_Definition(status_id=5, status_meaning="complete", test_status_id=5, test_status_meaning="Verified", specimen_status_id=2, specimen_status_meaning="specimen_accepted"),
            ]

            db.session.add_all(status_definitions)
            db.session.commit()
            logger.info("Status definitions populated successfully.")
        else:
            logger.info("Status definitions already exist. No action taken.")

    except Exception as e:
        logger.error(f"Error populating status definitions: {e}")
        db.session.rollback()

def populate_department_definitions():
    """
    Populates department definitions based on department information in the iBlis database.
    """
    department = application_config["department"]

    try:
        # Fetch the department ID from iBlis database
        result = iblis_session.execute(
            text("SELECT id FROM test_categories WHERE LCASE(name) = :department_name"),
            {"department_name": department.lower()}
        ).fetchone()

        if result:
            department_id = result[0]

            # Check if the department already exists in the main database
            existing_department = Department.query.filter_by(department_id=department_id).first()

            if not existing_department:
                # Create a new department record
                new_department = Department(
                    department_id=department_id,
                    department_name=department
                )
                db.session.add(new_department)
                db.session.commit()
                logger.info(f"Department '{department}' (ID: {department_id}) inserted successfully.")
            else:
                logger.info(f"Department '{department}' (ID: {department_id}) already exists in department_definitions.")
        else:
            logger.warning(f"Department '{department}' not found in test_categories table.")

    except Exception as e:
        logger.error(f"Error populating department definitions: {e}")
        db.session.rollback()
    finally:
        iblis_session.close()

def populate_test_definitions():
    """
    Populate test_definitions table in srsDB with data from test_types table in iBlissDB.
    """

    try:
        for test_type in test_types:
            # Fetch test definition from iBlissDB
            result = iblis_session.execute(
                text("SELECT id, name, short_name, targetTAT FROM test_types WHERE LCASE(short_name) = :test_type"),
                {"test_type": test_type.lower()}
            ).fetchone()

            if result:
                test_id, name, short_name, targetTAT = result

                # Check if entry already exists in srsDB
                existing_entry = db.session.query(Test_Definition).filter(
                    (Test_Definition.test_id == test_id) |
                    (Test_Definition.test_short_name == short_name)
                ).first()

                if not existing_entry:
                    # Add new test definition to srsDB
                    new_test_definition = Test_Definition(
                        test_id=test_id,
                        test_name=name,
                        test_short_name=short_name,
                        target_tat=targetTAT
                    )
                    db.session.add(new_test_definition)
                    db.session.commit()
                    logger.info(f"Test definition for '{name}' added successfully.")
                else:
                    logger.info(f"Test definition for '{name}' already exists. No action taken.")
            else:
                logger.warning(f"Test type '{test_type}' not found in iBlissDB.")

    except Exception as e:
        logger.error(f"Error populating test definitions: {e}")
        db.session.rollback()
    finally:
        # Close sessions
        iblis_session.close()


def populate_weekly_count():
    try:
        """Populate zeros in the department_id entities."""

        # varify the id against exists
        result = iblis_session.execute(
            text("SELECT test_category_id FROM test_types WHERE test_category_id = :department_id"),
            {"department_id": department_id}
        ).fetchone()

        # Check if the department_id entry does not already exist
        if result:
            existing_department_id = db.session.query(Weekly_Count).filter(
                Weekly_Count.department_id == department_id
            ).first()
            
            if not existing_department_id:

                # Create a new entry for Weekly_Count
                new_entry = Weekly_Count(department_id=department_id)
                db.session.add(new_entry)
                db.session.commit()
                logger.info(f"Weekly count entry for department {department_id} added successfully.")
            else:
                logger.info(f"Weekly count entry for department_id {department_id} already exists.")
        else:
            logger.warning(f"Invalid Department id {department_id} for {department}")
    except Exception as e:
        logger.error(f"Error populating weekly count: {e}")
        db.session.rollback()
    finally:
        iblis_session.close()

def populate_monthly_count():
    try:
        """Populate zeros in the test_id entities."""

        result = iblis_session.execute(
            text("SELECT test_category_id FROM test_types WHERE test_category_id = :department_id"),
            {"department_id": department_id}
        ).fetchone()

        if result:
            existing_department_id = db.session.query(Monthly_Count).filter(
                Monthly_Count.department_id == department_id
            ).first()
            
            if not existing_department_id:


                if not existing_department_id:
                    new_entry = Monthly_Count(department_id=department_id)
                    db.session.add(new_entry)
                    db.session.commit()
                    logger.info(f"monthly count entry for department_id {department_id} added successfully.")
            else:
                logger.info(f"monthly count entry for department_id {department_id} already exists.")
        else:
            logger.warning(f" invalid department id '{department_id}' not found in iBlissDB.")
    except Exception as e:
        logger.error(f"Error populating monthly count: {e}")
        db.session.rollback()
    finally:
        iblis_session.close()


# solving application context
if __name__ == "__main__":
    app = create_app()

    # Push the application context
    with app.app_context():
        populate_status_definitions()
        populate_department_definitions()
        populate_test_definitions()
        populate_weekly_count()
        populate_monthly_count()