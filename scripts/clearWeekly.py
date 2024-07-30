import mysql.connector
from mysql.connector import Error
import logging

# Configure logging
logging.basicConfig(filename='/home/ghii/Desktop/station/logs/database_operations.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

try:
    # Connect to the MySQL database
    connection = mysql.connector.connect(
        host="192.168.1.164",
        port="3306",
        user="ghii",
        password="..blackEvil89",
        database="Haematology",
	auth_plugin="mysql_native_password"
    )

    if connection.is_connected():
        cursor = connection.cursor()

        # Update all fields in the weekly_summary table to 0 where id = 1
        update_query = """
        UPDATE weekly_summary
        SET weekly_registered = 0, weekly_received = 0, weekly_progress = 0, weekly_pending = 0, weekly_complete = 0
        WHERE id = 1;
        """

        cursor.execute(update_query)
        connection.commit()
        logging.info("Weekly summary updated successfully")

except Error as e:
    logging.error(f"Error: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        logging.info("MySQL connection is closed")
