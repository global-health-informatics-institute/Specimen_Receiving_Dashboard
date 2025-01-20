import yaml
from extensions.extensions import db, department_data
from models.monthly_count_model import Monthly_Count


def extract_departments(data):
    """Extract departments as a list of dictionaries."""
    return [{'id': value['id']} for key, value in data.items()]

def seed_departments():
    """Seed the mothly_count table with data from the YAML file."""
    departments = extract_departments(department_data)
    try:
        for department in departments:
            new_department = Monthly_Count(
                department_id=department['id'], 
            )
            db.session.add(new_department)
        db.session.commit()
        print(f"Seeded {len(departments)} departments in the monthly counter.")
        return "Department data seeded successfully."
    except Exception as e:
        db.session.rollback()
        return f"Error occurred while seed"