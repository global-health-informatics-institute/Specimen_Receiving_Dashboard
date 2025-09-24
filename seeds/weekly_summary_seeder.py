from extensions.extensions import db, department_data, logger
from models.weekly_count_model import Weekly_Count


def extract_departments(data):
    """
    Extract departments as a list of dictionaries.
    :param data: Parsed YAML data.
    :return: List of department dictionaries.
    """
    return [{'id': value['id']} for key, value in data.items()]


def seed_weekly_count():
    """
    Seed the weekly_count table with data from the YAML file.
    """
    if not department_data:
        logger.error("No department data provided to seed.")
        return "No department data provided."

    departments = extract_departments(department_data)
    try:
        seeded_count = 0
        for department in departments:
            # Check if the department already exists in the weekly_count table
            existing_entry = Weekly_Count.query.filter_by(department_id=department['id']).first()
            if existing_entry:
                logger.info(f"Weekly count entry for department '{department['id']}' already exists. Skipping.")
                continue

            # Add new department entry to the monthly_count table
            new_department = Weekly_Count(department_id=department['id'])
            db.session.add(new_department)
            seeded_count += 1

        db.session.commit()
        return f"Seeded {seeded_count} departments in the weekly count table."
    except Exception as e:
        db.session.rollback()
        return (f"Error occurred while seeding weekly count data: {e}")


def run_weekly_count_seeder():
    seed_weekly_count()
