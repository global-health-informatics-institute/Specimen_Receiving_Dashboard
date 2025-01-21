from extensions.extensions import db, logger
from models.status_definitions_model import Test_Status_Definition

# Define the data to be seeded
test_status_definition_map = [
    (1, "registered", 2, "pending", 2, "specimen_accepted"),
    (2, "received", 3, "Started", 2, "specimen_accepted"),
    (3, "in_progress", 3, "started", 2, "specimen_accepted"),
    (4, "pending_auth", 4, "completed", 2, "specimen_accepted"),
    (5, "complete", 5, "verified", 2, "specimen_accepted")
]

def seed_test_status_definitions():
    """
    Seed the Test_Status_Definition table with predefined status data.
    """
    try:
        seed_count = 0
        for status in test_status_definition_map:
            # Unpack the tuple values into variables
            status_id, status_meaning, test_status_id, test_status_meaning, specimen_status_id, specimen_status_meaning = status

            if(Test_Status_Definition.query.filter_by(status_id=status_id).first()):
                logger.info(f"Test status definition '{status_id}' already exists. Skipping.")
                continue
            new_test_status_definition = Test_Status_Definition(
                status_id=status_id,
                status_meaning=status_meaning,
                test_status_id=test_status_id,
                test_status_meaning=test_status_meaning,
                specimen_status_id=specimen_status_id,
                specimen_status_meaning=specimen_status_meaning
            )
            seed_count+=1
            db.session.add(new_test_status_definition)


        db.session.commit()
        logger.info(f"Seeded {(seed_count)} test status definitions.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error occurred while seeding test status definitions: {e}")

def run_test_status_definitions_seeder():
     seed_test_status_definitions()
