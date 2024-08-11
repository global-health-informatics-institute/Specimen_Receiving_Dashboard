from mysql.connector import Error
import logging
from models.config import srsDB

# Configure logging
log_file_path = '/home/ghii/Desktop/opz/logs/database_operations.log'
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s %(levelname)s:%(message)s')

try:
    # Ensure the log directory exists
    import os
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    # Connect to the MySQL database
    srsConnection = srsDB()  # Get the connection object by calling the function

    if srsConnection and srsConnection.is_connected():
        cursor = srsConnection.cursor()

        # Update all fields in the weekly_summary table to 0 where id = 1
        update_query = """
        UPDATE weekly_summary
        SET weekly_registered = 0, weekly_received = 0, weekly_progress = 0, weekly_pending = 0, weekly_complete = 0, weekly_rejected = 0 
        WHERE id = 1;
        """

        cursor.execute(update_query)
        srsConnection.commit()
        logging.info("Weekly summary updated successfully")

except Error as e:
    logging.error(f"Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'srsConnection' in locals() and srsConnection.is_connected():
        srsConnection.close()
        logging.info("MySQL connection is closed")

