import os
import mysql.connector
import sqlite3

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR,'intermediateDB.db')
# name of department the system is set up in
department = "Haematology"

# short name for the tests that needs to be displayed (4)
testType1 = "FBC"
testType2 = "PT"
testType3 = "APTT"
testType4 = "INR"

# how many days do you need the test to be alive
interval = 1

# Screen name equal to view name (departmentName+screenNumber)
screenName = "Haematology1"

# MySQL config depending on server properties
mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="root",
    database="tests"
)

def getTestTypeId(testType):
    try:
        # Connect to your SQLite database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        query = 'SELECT test_id FROM test_definitions WHERE lower(test_short_name) = ?;'
        cursor.execute(query, (testType.lower(),))  # Make sure this is a tuple
        result = cursor.fetchone()
        test_id = result[0] if result else 0
        return test_id
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    finally:
        if 'conn' in locals() and conn:
            conn.close()
