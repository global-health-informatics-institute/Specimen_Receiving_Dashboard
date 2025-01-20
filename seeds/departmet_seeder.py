import yaml
from extensions.extensions import db, department_data
from models.department_model import Department


def extract_departments(data):
    """Extract departments as a list of dictionaries."""
    return [{'id': value['id'], 'name': value['name']} for key, value in data.items()]

def seed_departments():
    """Seed the departments table with data from the YAML file."""
    departments = extract_departments(department_data)
    try:
        for department in departments:
            new_department = Department(
                department_id=department['id'], 
                department_name=department['name']
            )
            db.session.add(new_department)
        db.session.commit()
        print(f"Seeded {len(departments)} departments.")
        return "Department data seeded successfully."
    except Exception as e:
        db.session.rollback()
        return f"Error occurred while seed"