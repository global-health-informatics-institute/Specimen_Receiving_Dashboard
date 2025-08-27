import json
import yaml
from extensions.extensions import iblis_db

# Paths for input and output files
input_json_file = 'data/iblis_test_types.json'
output_yaml_file = 'data/test_types.yml'

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
            "id": item["_id"],
            "name": item["name"],
            "department_id": item["department_id"],
            "test_type_id": item["test_type_id"]
        }

    # Save the transformed data to a YAML file
    with open(output_file, 'w') as f:
        yaml.dump(formatted_data, f, default_flow_style=False, sort_keys=False)

    print(f"Data transformed and saved to {output_file}.")


# Step 2: Retrieve TAT data from the database
def retrieve_tat_data():
    """
    Retrieve targetTAT values from the test_types table in the database.
    Returns a dictionary mapping test type names to their targetTAT.
    """
    try:
        connection = iblis_db()
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT name, targetTAT FROM test_types")
        tat_data = {row['name']: row['targetTAT'] for row in cursor.fetchall()}
    except Exception as e:
        print(f"Error retrieving TAT data: {e}")
        tat_data = {}
    finally:
        cursor.close()
        connection.close()

    return tat_data


# Step 3: Append TAT data to the YAML file
def append_tat_to_yaml(input_file, output_file):
    """
    Append targetTAT values from the database to the YAML file.
    """
    # Load YAML data
    with open(input_file, 'r') as f:
        yaml_data = yaml.safe_load(f)

    # Fetch TAT data from the database
    tat_data = retrieve_tat_data()

    # Update YAML data with TAT values
    for test_name, details in yaml_data.items():
        if test_name in tat_data:
            details['tat'] = tat_data[test_name]  # Append TAT to the YAML entry

    # Save the updated YAML data
    with open(output_file, 'w') as f:
        yaml.dump(yaml_data, f, default_flow_style=False, sort_keys=False)

    print(f"TAT values successfully appended to {output_file}.")


# Main execution
if __name__ == "__main__":
    # Step 1: Transform JSON to YAML
    transform_json_to_yaml(input_json_file, output_yaml_file)

    # Step 2: Append TAT data to YAML
    append_tat_to_yaml(output_yaml_file, output_yaml_file)
