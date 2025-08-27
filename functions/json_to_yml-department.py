import json
import yaml
from extensions.extensions import iblis_db

# Paths for input and output files
input_json_file = 'data/iblis_departments.json'
output_yaml_file = 'data/departments.yml'

# Step 1: Transform JSON data to YAML format
def transform_json_to_yaml(input_file, output_file):
    """
    Transforms JSON data into a structured YAML format.
    """
    # Read the JSON file
    with open(input_file, 'r') as f:
        data = json.load(f)

    # Transform the data into the desired YAML format
    formatted_data = {}
    for item in data:
        key = item['_id']
        formatted_data[key] = {
            "id": item["id"],
            "name": item["name"],
        }

    # Save the transformed data to a YAML file
    with open(output_file, 'w') as f:
        yaml.dump(formatted_data, f, default_flow_style=False, sort_keys=False)

    print(f"Data transformed and saved to {output_file}.")


# Step 2: Retrieve department ids from the database
def retrieve_department_data():
    """
    Retrieve department ids values from the test_types table in the database.
    Returns a dictionary mapping department names to their ids.
    """
    try:
        connection = iblis_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT name, id FROM test_categories")
        department_data = {row['name']: row['id'] for row in cursor.fetchall()}
    except Exception as e:
        print(f"Error retrieving department data: {e}")
        department_data = {}
    finally:
        cursor.close()
        connection.close()

    return department_data


# Step 3: Append id data to the YAML file
def append_tat_to_yaml(input_file, output_file):
    """
    Append department id values from the database to the YAML file.
    """
    # Load YAML data
    with open(input_file, 'r') as f:
        yaml_data = yaml.safe_load(f)

    # Fetch TAT data from the database
    department_data = retrieve_department_data()

    # Update YAML data with TAT values
    for department_name, details in yaml_data.items():
        if department_name in department_data:
            details['department_id'] = department_data[department_name]

    # Save the updated YAML data
    with open(output_file, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)

    print(f"department id values successfully appended to {output_file}.")


# Main execution
if __name__ == "__main__":
    # Step 1: Transform JSON to YAML
    transform_json_to_yaml(input_json_file, output_yaml_file)

    # Step 2: Append TAT data to YAML
    append_tat_to_yaml(output_yaml_file, output_yaml_file)
