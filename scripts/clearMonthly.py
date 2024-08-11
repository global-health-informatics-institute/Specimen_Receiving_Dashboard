from mysql.connector import Error
import logging
from models.config import srsDB

# Configure logging
logging.basicConfig(filename='/home/eight/Desktop/GHII/optimized/logs/database_operations.log', level=logging.INFO,
                    format='%(asctime)s %(levelname)s:%(message)s')

try:
    # Connect to the MySQL database
    srsConnection = srsDB()  # Get the connection object by calling the function

    if srsConnection and srsConnection.is_connected():
        cursor = srsConnection.cursor()

        # Update all fields in the monthly_summary table to 0 where id = 1
        update_query = """
        UPDATE monthly_summary
        SET monthly_registered = 0, monthly_received = 0, monthly_progress = 0, monthly_pending = 0, monthly_complete = 0
        WHERE id = 1;
        """

        cursor.execute(update_query)
        srsConnection.commit()
        logging.info("Monthly summary updated successfully")

except Error as e:
    logging.error(f"Error: {e}")
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'srsConnection' in locals() and srsConnection.is_connected():
        srsConnection.close()
        logging.info("MySQL connection is closed")
