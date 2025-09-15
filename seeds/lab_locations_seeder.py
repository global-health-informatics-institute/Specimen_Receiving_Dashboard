from extensions.extensions import db, lab_location_data, logger
from models.lab_location_model import Lab_Location


def extract_lab_locations(data):
    """
    Extract lab locations as a list of dictionaries.
    :param data: Parsed YAML data.
    :return: List of lab location dictionaries.
    """
    return [{'id': value['id'], 'name': value['name']} for key, value in data.items()]

def seed_lab_locations(lab_location_data):
    """
    Seed the lab locations table with data.
    :param lab_location_data: List of lab location dictionaries.
    """
    try:
        for lab_location in lab_location_data:
            existing_lab_location = Lab_Location.query.filter_by(lab_location_id=lab_location['id']).first()
            if existing_lab_location:
                logger.warning(f"Lab Location '{lab_location['id']}' already exists. Skipping.")
                continue

            # Add new lab location
            new_lab_location = Lab_Location(
                lab_location_id=lab_location['id'],
                lab_location_name=lab_location['name']
            )
            db.session.add(new_lab_location)

        db.session.commit()
        logger.info(f"Seeded {len(lab_location_data)} lab locations successfully.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error occurred while seeding lab locations: {e}")


def run_lab_location_seeder():
    extracted_lab_locations = extract_lab_locations(lab_location_data)
    seed_lab_locations(extracted_lab_locations)
