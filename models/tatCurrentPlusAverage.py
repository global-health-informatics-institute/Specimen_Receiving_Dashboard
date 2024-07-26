import mysql.connector
from mysql.connector import Error
from models.helper import getTestTypeID

def iBlissDB():
    try: 
        connection = mysql.connector.connect(
            host="192.168.1.164",
            port="3306",
            user="ghii",
            password="..blackEvil89",
            database="tests",
            auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            print("Successfully connected to IBliss database")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

def tatCurrent(test_type):
    connection = iBlissDB()
    if connection is None:
        print("Failed to connect to srsDB.")
        return ""
    else:
        iBlissCursor = connection.cursor()
    
    try:
        if iBlissCursor:
            query = """
                SELECT 
                    IFNULL(ROUND(AVG(TIMESTAMPDIFF(MINUTE, time_started, time_completed)), 2), 0) AS average_duration_in_hours
                FROM 
                    tests
                WHERE 
                    time_started IS NOT NULL 
                    AND time_completed IS NOT NULL
                    AND tests.time_created >= CURDATE() + INTERVAL 7 HOUR
                    AND tests.time_created <= CURDATE() + INTERVAL 1 DAY + INTERVAL 7 HOUR 
                    AND test_type_id = %s;
            """
            iBlissCursor.execute(query, (getTestTypeID(test_type),))
            result = iBlissCursor.fetchone()
            if result:
                return result[0]  # Return the average duration in hours
            else:
                print("No result found.")
                return ""
        else:
            print("Cursor not initialized.")
            return ""
    except Error as e:
        print(f"Error: {e}")
    finally:
        if iBlissCursor:
            iBlissCursor.close()
        if connection and connection.is_connected():
            connection.close()

# Example usage:
# result = tatCurrent("35")
# print(result)


def tatAverage(test_type):
    connection = iBlissDB()
    if connection is None:
        print("Failed to connect to srsDB.")
        return ""
    else:
        iBlissCursor = connection.cursor()
    
    try:
        if iBlissCursor:
            query = """
                SELECT 
                    IFNULL(ROUND(AVG(TIMESTAMPDIFF(HOUR, time_started, time_completed)), 2), 0) AS average_duration_in_hours
                FROM 
                    tests
                WHERE
                    time_started IS NOT NULL 
                    AND time_completed IS NOT NULL
                    AND test_status_id NOT IN (8.6,7)
                    AND time_started >= DATE_ADD(DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY), INTERVAL 7 HOUR)
                    AND time_started < DATE_ADD(DATE_SUB(CURDATE(), INTERVAL WEEKDAY(CURDATE()) DAY) + INTERVAL 7 DAY, INTERVAL 7 HOUR)
                    AND test_type_id = %s;        
            """
            iBlissCursor.execute(query, (getTestTypeID(test_type),))
            result = iBlissCursor.fetchone()
            if result:
                print(f"AVERAGE is {result}")
                return result[0]  # Return the average duration in hours
            else:
                print("No result found.")
                return ""
        else:
            print("Cursor not initialized.")
            return ""
    except Error as e:
        print(f"Error: {e}")
    finally:
        if iBlissCursor:
            iBlissCursor.close()
        if connection and connection.is_connected():
            connection.close()

# Example usage:
# result = tatCurrent("35")
# print(result)
