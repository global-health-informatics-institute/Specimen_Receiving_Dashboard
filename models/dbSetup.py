import sqlite3
import mysql.connector

# Manually pass on for including the department
department = "Haematology"
testType1 = "FBC"
testType2 = "PT"
testType3 = "APTT"
testType4 = "INR"

# MySQL config depending on server properties
mydb = mysql.connector.connect(
    host="127.0.0.1",
    port="3306",
    user="root",
    password="@clk11CK",
    database="test"
)

def fetchDepartmentDefinitions(department):
    try:
        mycursor = mydb.cursor()
        # Fetch department ID from MySQL
        mycursor.execute(f"SELECT id FROM test_categories WHERE LCASE(name) = '{department.lower()}'")
        result = mycursor.fetchone()
        
        if result:
            department_id = result[0]
            # Insert into SQLite
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO department_definitions(department_id, department_name) 
                VALUES (?, ?)
            ''', (department_id, department))
            conn.commit()
            conn.close()
        else:
            print(f"No department found for {department}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")

def fetchTestDefinitions(testType):
    try:
        mycursor = mydb.cursor()
        # Fetch test details from MySQL
        mycursor.execute(f"SELECT id, name, short_name, targetTAT FROM test_types WHERE LCASE(short_name) = '{testType.lower()}'")
        result = mycursor.fetchone()
        
        if result:
            test_id, name, short_name, targetTAT = result
            # Insert into SQLite
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO test_definitions(test_id, test_name, test_short_name, targetTAT) 
                VALUES (?, ?, ?, ?)
            ''', (test_id, name, short_name, targetTAT))
            conn.commit()
            conn.close()
        else:
            print(f"No test found for {testType}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")


def populateStatusDefinitions(
    statusId,
    statusName,
    testStatusId,
    testStatusName,
    specimenStatusId,
    specimenStatusName
):
    try:
        # Insert into SQLite
        conn = sqlite3.connect('models/intermediateDB.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO status_definitions(
                status_id,
                status_name,
                test_status_id,
                test_status_name,
                specimen_status_id,
                specimen_status_name
            ) 
            VALUES (?, ?, ?, ?, ?, ?)
        ''',
            (
                statusId,
                statusName,
                testStatusId,
                testStatusName,
                specimenStatusId,
                specimenStatusName
            ) 
        )
        conn.commit()
        conn.close()
    except sqlite3.Error as err:
        print(f"Error: {err}")

def dbSetup():
    try:
        # DB connection
        conn = sqlite3.connect('models/intermediateDB.db')

        # cursor Object
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS department_definitions(
                id INTEGER NOT NULL UNIQUE,
                department_id INTEGER NOT NULL,
                department_name VARCHAR(100) NOT NULL,  
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        # Check if the department_definitions table was just created
        cursor.execute("SELECT COUNT(*) FROM department_definitions")
        if cursor.fetchone()[0] == 0:
            fetchDepartmentDefinitions(department)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_definitions(
                id INTEGER NOT NULL UNIQUE,
                test_id INTEGER NOT NULL,
                test_name VARCHAR(100) NOT NULL,
                test_short_name VARCHAR(100) NOT NULL,
                targetTAT VARCHAR(100) NOT NULL,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        # Check if the test_definitions table was just created
        cursor.execute("SELECT COUNT(*) FROM test_definitions")
        if cursor.fetchone()[0] == 0:
            fetchTestDefinitions(testType1)
            fetchTestDefinitions(testType2)
            fetchTestDefinitions(testType3)
            fetchTestDefinitions(testType4)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status_definitions(
                id INTEGER NOT NULL UNIQUE,
                status_id INTEGER NOT NULL,
                status_name VARCHAR(100) NOT NULL,
                test_status_id INTEGER NOT NULL,
                test_status_name VARCHAR(100) NOT NULL,
                specimen_status_id INTEGER NOT NULL,
                specimen_status_name VARCHAR(100) NOT NULL,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')
        cursor.execute("SELECT COUNT(*) FROM status_definitions")
        if cursor.fetchone()[0] == 0:
            populateStatusDefinitions(1,"registered",2,"Pending",2,"specimen_accepted")
            populateStatusDefinitions(2,"Received",3,"Started",2,"specimen_accepted")
            populateStatusDefinitions(3,"registered",3,"Started",2,"specimen_accepted")
            populateStatusDefinitions(4,"registered",4,"Completed",2,"specimen_accepted")
            populateStatusDefinitions(5,"registered",5,"Verified",2,"specimen_accepted")



        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER NOT NULL UNIQUE,
                assertion_id INTEGER NOT NULL,
                test_type VARCHAR(100) NOT NULL,
                test_status VARCHAR(100) NOT NULL,
                write_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_summary (
                id INTEGER NOT NULL UNIQUE,
                weekly_registered INTEGER,
                weekly_received INTEGER,
                weekly_progress INTEGER,
                weekly_pending INTEGER ,
                weekly_complete INTEGER ,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_summary (
                id INTEGER NOT NULL UNIQUE,
                monthly_registered INTEGER,
                monthly_received INTEGER,
                monthly_progress INTEGER,
                monthly_pending INTEGER,
                monthly_complete INTEGER,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()

# Call the function to set up the database
dbSetup()
