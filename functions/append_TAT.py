import yaml
import mysql.connector

# Load configuration from YAML
with open("config/application.config.yml", 'r') as config_file:
    config = yaml.safe_load(config_file)

# Database connection function
def db():
    """Create a database connection using the configuration."""
    db_config = config['application_config']['iblis']
    return mysql.connector.connect(
        host=db_config['host'],
        port=db_config['port'],
        user=db_config['user'],
        password=db_config['password'],
        database=db_config['database'],
        auth_plugin=db_config.get('auth_plugin', 'mysql_native_password')
    )

# Load TAT data from the database
def retrieve_tat_data():
    """
    Retrieve targetTAT values from the test_types table in the database.
    Returns a dictionary mapping test type names to their targetTAT.
    """
    connection = db()
    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT name, targetTAT FROM test_types")
    tat_data = {row['name']: row['targetTAT'] for row in cursor.fetchall()}
    cursor.close()
    connection.close()
    return tat_data

# Update YAML file with TAT data
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

# Main execution
if __name__ == "__main__":
    input_file = 'data/test_types.yml'
    output_file = 'data/test_types.yml'
    append_tat_to_yaml(input_file, output_file)
    print(f"TAT values successfully appended to {output_file}.")
