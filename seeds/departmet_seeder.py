from extensions.extensions import db, department_data, logger
from models.department_model import Department


def extract_departments(data):
    """
    Extract departments as a list of dictionaries.
    :param data: Parsed YAML data.
    :return: List of department dictionaries.
    """
    return [{'id': value['id'], 'name': value['name']} for key, value in data.items()]

def seed_departments(department_data):
    """
    Seed the departments table with data.
    :param department_data: List of department dictionaries.
    """
    try:
        for department in department_data:
            existing_department = Department.query.filter_by(department_id=department['id']).first()
            if existing_department:
                logger.warning(f"Department '{department['id']}' already exists. Skipping.")
                continue

            # Add new department
            new_department = Department(
                department_id=department['id'],
                department_name=department['name']
            )
            db.session.add(new_department)

        db.session.commit()
        logger.info(f"Seeded {len(department_data)} departments successfully.")
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error occurred while seeding departments: {e}")


def run_department_seeder():
    extracted_departments = extract_departments(department_data)
    seed_departments(extracted_departments)
