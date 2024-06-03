# ToDo: implement the following: fetch data from IBlisDB within 3 days, move it to intermediate migrateAll()
# ToDo: update summaryData()
# ToDo: update tests()
# ToDo: update weekly_summary()
# ToDo: update monthly_summary()

from config import *
import sqlite3

def migrateAllUnique(screenName):
    try:
        # Connect to MySQL database
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT * FROM {screenName}")
        result = mycursor.fetchall()

        if result:
            # Connect to SQLite database
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()

            for row in result:
                # Assume the structure of the row and columns
                accession_id, test_type, test_status = row

                # Check if the record already exists in SQLite
                cursor.execute('''
                    SELECT COUNT(*) FROM tests WHERE accession_id = ?
                ''', (accession_id,))
                exists = cursor.fetchone()[0]

                if exists == 0:
                    # If record does not exist, insert it
                    cursor.execute('''
                        INSERT INTO tests ( accession_id, test_type, test_status) 
                        VALUES (?, ?, ?)
                    ''', ( accession_id, test_type, test_status))

            conn.commit()
    except mysql.connector.Error as err:
        print(f"MySQL Error: {err}")
    except sqlite3.Error as err:
        print(f"SQLite Error: {err}")
    finally:
        # Close the connections
        if mycursor:
            mycursor.close()
        if conn:
            conn.close()
# Call the function with your screenName
migrateAllUnique(screenName)
