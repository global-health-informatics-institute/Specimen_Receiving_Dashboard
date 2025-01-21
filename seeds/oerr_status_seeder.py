from extensions.extensions import db, logger
from models.oerr_status_model import OERR_Status_Definition

# Define the data to be seeded
oerr_status_map = [
    (1, "registered"),
    (2, "received"),
    (3, "in_progress"),
    (4, "pending_auth"),
    (5, "completed"),
    (0, "rejected")
]

def seed_oerr_status_definitions():
    """
    Seed the OERR_Status table with predefined status data.
    """
    try:
        seed_count = 0
        for status in oerr_status_map:
            # Unpack the tuple values into variables
            oerr_status_id, oerr_status_meaning = status

            if(OERR_Status_Definition.query.filter_by(oerr_status_id=oerr_status_id).first()):
                logger.info(f"OERR status definition '{oerr_status_id}' already exists. Skipping.")
                continue
            new_oerr_status_definition = OERR_Status_Definition(
                oerr_status_id=oerr_status_id,
                oerr_status_meaning=oerr_status_meaning,
            )
            seed_count+=1
            db.session.add(new_oerr_status_definition)


        db.session.commit()
        logger.info(f"Seeded {(seed_count)} oerr status definitions.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error occurred while seeding oerr status definitions: {e}")

def run_oerr_status_definitions_seeder():
     seed_oerr_status_definitions()
