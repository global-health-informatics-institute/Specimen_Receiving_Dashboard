from config import mydb, screenName
import mysql.connector
import sqlite3
import logging

logging.basicConfig(level=logging.INFO)

def migrateAllUnique(screenName):
    try:
        mycursor = mydb.cursor()

        mycursor.execute(f"SELECT * FROM {screenName}")
        result = mycursor.fetchall()

        if result:
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()

            for row in result:
                accession_id, test_type, test_status = row

                cursor.execute('SELECT COUNT(*) FROM tests WHERE accession_id = ?', (accession_id,))
                exists = cursor.fetchone()[0]

                if exists == 0:
                    cursor.execute('INSERT INTO tests (accession_id, test_type, test_status) VALUES (?, ?, ?)', (accession_id, test_type, test_status))

            conn.commit()
            conn.close()
    except mysql.connector.Error as err:
        logging.error(f"MySQL Error: {err}")
    except sqlite3.Error as err:
        logging.error(f"SQLite Error: {err}")
    finally:
        if mycursor:
            mycursor.close()

# try:
#     migrateAllUnique(screenName)
# except Exception as e:
#     logging.error(f"An error occurred: {e}")
def updateExisting():
    try:
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM {screenName}")
        result = mycursor.fetchall()

        if result:
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()

            for row in result:
                accession_id, test_type, test_status = row

                # Check if the accession_id already exists in the SQLite database
                cursor.execute('SELECT test_status FROM tests WHERE accession_id = ?', (accession_id,))
                existing_record = cursor.fetchone()

                if existing_record:
                    existing_status = int(existing_record[0])  # Convert to integer for comparison
                    test_status = int(test_status)  # Ensure test_status is an integer

                    # Update the record only if necessary
                    if existing_status != test_status and not (test_status == 3 and existing_status < 3):
                        cursor.execute(
                            'UPDATE tests SET test_status = ?, test_type = ? WHERE accession_id = ?',
                            (test_status, test_type, accession_id)
                        )
                else:
                    # Insert a new record if it doesn't exist
                    cursor.execute(
                        'INSERT INTO tests (accession_id, test_type, test_status) VALUES (?, ?, ?)',
                        (accession_id, test_type, test_status)
                    )

            conn.commit()

    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
    except sqlite3.Error as e:
        print(f"Error connecting to SQLite database: {e}")
    except ValueError as e:
        print(f"Value error: {e}")
    finally:
        if mycursor:
            mycursor.close()
        if conn:
            conn.close()

# Call the function to update existing records
updateExisting()
