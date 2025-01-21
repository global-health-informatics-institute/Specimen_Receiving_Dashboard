from extensions.extensions import db, test_type_data, logger
from models.test_definitions_model import Test_Definition


def extract_test_types(data):
    """
    Extract test_types as a list of dictionaries.
    :param data: Parsed YAML data.
    :return: List of test type dictionaries.
    """
    return [
        {
            'id': value['id'],
            'name': value['name'],
            'test_type_id': value['test_type_id'],
            'tat': value.get('tat', None),
            'department_id': value['department_id']
        }
        for key, value in data.items()
    ]


def seed_test_types():
    """
    Seed the test_types table with data from the YAML file.
    """
    if not test_type_data:
        return "No test type data provided."

    test_types = extract_test_types(test_type_data)
    try:
        seeded_count = 0
        for test_type in test_types:
            # Check if the test type already exists
            existing_test = Test_Definition.query.filter_by(test_id=test_type['test_type_id']).first()
            if existing_test:
                logger.info(f"Test type '{test_type['test_type_id']}' already exists. Skipping.")
                continue

            # Add new test type
            new_test_type = Test_Definition(
                test_id=test_type['test_type_id'],
                test_name=test_type['id'],
                test_short_name=test_type['name'],
                target_tat=test_type['tat'],
                test_department_id=test_type['department_id']
            )
            db.session.add(new_test_type)
            seeded_count += 1

        db.session.commit()
        return f"Seeded {seeded_count} new test types successfully."
    except Exception as e:
        db.session.rollback()
        logger.error(f"Error occurred while seeding test types: {e}")
        return f"Error occurred while seeding test types: {e}"


def run_test_type_seeder():
    seed_test_types()
    
