from models.config import mydb, screenName
import mysql.connector
import sqlite3
import logging
from models.weeklyData import WeeklyIncrementor
from models.monthlyData import MonthlyIncrementor

logging.basicConfig(level=logging.INFO)

def migrateAllUnique():
    try:
        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM {screenName}")
        result = mycursor.fetchall()

        if result:
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()
            
            weekly_incrementor = WeeklyIncrementor()
            monthly_incrementor = MonthlyIncrementor()

            new_records_count = 0

            for row in result:
                accession_id, test_type, test_status = row

                if test_status != 5:
                    cursor.execute('SELECT COUNT(*) FROM tests WHERE accession_id = ?', (accession_id,))
                    exists = cursor.fetchone()[0]

                    if exists == 0:
                        cursor.execute('INSERT INTO tests (accession_id, test_type, test_status) VALUES (?, ?, ?)', (accession_id, test_type, test_status))
                        new_records_count += 1
                        
                        if test_status == 2:
                            weekly_incrementor.incrementRegistered()
                            monthly_incrementor.incrementRegistered()
                        elif test_status == 3:
                            weekly_incrementor.incrementInprogress()
                            monthly_incrementor.incrementInprogress()
                        elif test_status == 4:
                            weekly_incrementor.incrementPendingAuth()
                            monthly_incrementor.incrementPendingAuth()

            conn.commit()
            conn.close()
            weekly_incrementor.closeConn()
            monthly_incrementor.closeConn()

            logging.info(f"New records inserted: {new_records_count}")
    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
    except sqlite3.Error as err:
        logging.error(f"SQLite Error: {err}")
    finally:
        if mycursor:
            mycursor.close()


def updateExisting():
    try:
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM {screenName}")
        result = mycursor.fetchall()

        if result:
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()
            
            weekly_incrementor = WeeklyIncrementor()
            monthly_incrementor = MonthlyIncrementor()

            updated_records_count = 0
            inserted_records_count = 0

            for row in result:
                accession_id, test_type, test_status = row

                # Check if the accession_id already exists in the SQLite database
                cursor.execute('SELECT test_status FROM tests WHERE accession_id = ?', (accession_id,))
                existing_record = cursor.fetchone()

                if existing_record:
                    existing_status = int(existing_record[0])  # Convert to integer for comparison
                    test_status = int(test_status)  # Ensure test_status is an integer

                    if existing_status == 0 and test_status in [1, 2, 3]:
                        continue  # Skip updating if the current status is 0 and the new status is 1, 2, or 3

                    # Update the record if necessary
                    if existing_status != test_status:
                        cursor.execute(
                            'UPDATE tests SET test_status = ?, test_type = ? WHERE accession_id = ?',
                            (test_status, test_type, accession_id)
                        )
                        updated_records_count += 1
                        
                        if test_status == 2:
                            weekly_incrementor.incrementRegistered()
                            monthly_incrementor.incrementRegistered()
                        elif test_status == 3:
                            weekly_incrementor.incrementInprogress()
                            monthly_incrementor.incrementInprogress()
                        elif test_status == 4:
                            weekly_incrementor.incrementPendingAuth()
                            monthly_incrementor.incrementPendingAuth()
                        elif test_status == 5:
                            weekly_incrementor.incrementComplete()
                            monthly_incrementor.incrementComplete()

                else:
                    # Insert a new record if it doesn't exist and the fetched record does not have test_status of 5
                    if test_status != 5:
                        cursor.execute(
                            'INSERT INTO tests (accession_id, test_type, test_status) VALUES (?, ?, ?)',
                            (accession_id, test_type, test_status)
                        )
                        inserted_records_count += 1
                        
                        if test_status == 2:
                            weekly_incrementor.incrementRegistered()
                            monthly_incrementor.incrementRegistered()
                        elif test_status == 3:
                            weekly_incrementor.incrementInprogress()
                            monthly_incrementor.incrementInprogress()
                        elif test_status == 4:
                            weekly_incrementor.incrementPendingAuth()
                            monthly_incrementor.incrementPendingAuth()

            conn.commit()
            weekly_incrementor.closeConn()
            monthly_incrementor.closeConn()
            
            logging.info(f"Records updated: {updated_records_count}")
            logging.info(f"Records inserted: {inserted_records_count}")

    except mysql.connector.Error as e:
        logging.error(f"Error connecting to MySQL database: {e}")
    except sqlite3.Error as e:
        logging.error(f"Error connecting to SQLite database: {e}")
    except ValueError as e:
        logging.error(f"Value error: {e}")
    finally:
        if mycursor:
            mycursor.close()
        if conn:
            conn.close()

