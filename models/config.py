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

# at wat time should the dashboard clear itselfe
time_out = 7

# MySQL Iblis config depending on server properties
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


# MySQL config as for SRS
def srsDB():
    try:
        connection = mysql.connector.connect(
            host="192.168.1.164",
            port="3306",
            user="ghii",
            password="..blackEvil89",
            database=department,
            auth_plugin='mysql_native_password'
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
        host="192.168.1.164",
        port="3306",
        user="ghii",
        password="..blackEvil89",
        auth_plugin='mysql_native_password'
        )
        if connection.is_connected():
            print("Successfully connected to server")
            return connection
    except Error as e:
        print(f"Error: {e}")
        return None

