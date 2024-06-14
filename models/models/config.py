import mysql.connector
from mysql.connector import Error

# name of department the system is set up in, Represent the join & view
department = "Haematology"

# short name for the tests that needs to be displayed (4). Unlike having seperate view, data ll be fetched using test IDs
testType1 = "FBC"
testType2 = "PT"
testType3 = "APTT"
testType4 = "INR"

# how many days do you need the test to be alive
interval = 1

# MySQL Iblis config depending on server properties
def iBlissDB():
    try: 
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="root",
            database="tests"
        )
        if connection.is_connected():
            print("Successfully connected to IBliss database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None


# MySQL config as for SRS
def srsDB():
    try:
        connection = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="root",
            database=department
        )
        if connection.is_connected():
            print("Successfully connected to the database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

# SRS MySQL connect only obj for 
def srsDBConn():
    try:
        connection = mysql.connector.connect(
        host="127.0.0.1",
        port="3306",
        user="root",
        password="root",
        )
        if connection.is_connected():
            print("Successfully connected to server")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None



# def getTestTypeId(testType):
#     try:
#         # Connect to your SQLite database
#         conn = sqlite3.connect(db_path)
#         cursor = conn.cursor()
#         query = 'SELECT test_id FROM test_definitions WHERE lower(test_short_name) = ?;'
#         cursor.execute(query, (testType.lower(),))  # Make sure this is a tuple
#         result = cursor.fetchone()
#         test_id = result[0] if result else 0
#         return test_id
#     except sqlite3.Error as e:
#         print(f"Error connecting to database: {e}")
#         return None
#     finally:
#         if 'conn' in locals() and conn:
#             conn.close()
