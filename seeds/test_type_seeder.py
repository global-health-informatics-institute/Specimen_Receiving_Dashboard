import yaml
from extensions.extensions import db, test_type_data
from models.test_definitions_model import Test_Definition


def extract_test_types(data):
    """Extract test_types as a list of dictionaries."""
    return [{'id': value['id'], 'name': value['name']} for key, value in data.items()]

def seed_test_types():
    """Seed the test typed table with data from the YAML file."""
    test_types = extract_test_types(test_type_data)
    try:
        for test_type in test_types:
            new_test_type = Test_Definition(
                test_id=test_type['test_type_id'], 
                test_name=test_type['id'],
                test_short_name= test_type['name'],
                target_tat= test_type['tat'],
                test_department = test_type['department_id']
            )
            db.session.add(new_test_type)
        db.session.commit()
        print(f"Seeded {len(test_types)} test references.")
        return "Test data seeded successfully."
    except Exception as e:
        db.session.rollback()
        return f"Error occurred while seed"
