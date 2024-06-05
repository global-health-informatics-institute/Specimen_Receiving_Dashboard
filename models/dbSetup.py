import sqlite3
from config import *

def fetchDepartmentDefinitions(department):
    try:
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT id FROM test_categories WHERE LCASE(name) = '{department.lower()}'")
        result = mycursor.fetchone()
        
        if result:
            department_id = result[0]
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO department_definitions(department_id, department_name) 
                VALUES (?, ?)
            ''', (department_id, department))
            conn.commit()
        else:
            print(f"No department found for {department}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn:
            conn.close()
        if mycursor:
            mycursor.close()

def fetchTestDefinitions(testType):
    try:
        mycursor = mydb.cursor()
        mycursor.execute(f"SELECT id, name, short_name, targetTAT FROM test_types WHERE LCASE(short_name) = '{testType.lower()}'")
        result = mycursor.fetchone()
        
        if result:
            test_id, name, short_name, targetTAT = result
            conn = sqlite3.connect('models/intermediateDB.db')
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO test_definitions(test_id, test_name, test_short_name, targetTAT) 
                VALUES (?, ?, ?, ?)
            ''', (test_id, name, short_name, targetTAT))
            conn.commit()
        else:
            print(f"No test found for {testType}")
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if conn:
            conn.close()
        if mycursor:
            mycursor.close()

def populateStatusDefinitions(statusId, statusName, testStatusId, testStatusName, specimenStatusId, specimenStatusName):
    try:
        conn = sqlite3.connect('models/intermediateDB.db')
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO status_definitions(
                status_id, status_name, test_status_id, test_status_name, specimen_status_id, specimen_status_name
            ) VALUES (?, ?, ?, ?, ?, ?)
        ''', (statusId, statusName, testStatusId, testStatusName, specimenStatusId, specimenStatusName))
        conn.commit()
    except sqlite3.Error as err:
        print(f"Error: {err}")
    finally:
        if conn:
            conn.close()

def dbSetup():
    try:
        conn = sqlite3.connect('models/intermediateDB.db')
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS department_definitions (
                id INTEGER NOT NULL UNIQUE,
                department_id INTEGER NOT NULL,
                department_name VARCHAR(100) NOT NULL,  
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        cursor.execute("SELECT COUNT(*) FROM department_definitions")
        if cursor.fetchone()[0] == 0:
            fetchDepartmentDefinitions(department)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS test_definitions (
                id INTEGER NOT NULL UNIQUE,
                test_id INTEGER NOT NULL,
                test_name VARCHAR(100) NOT NULL,
                test_short_name VARCHAR(100) NOT NULL,
                targetTAT VARCHAR(100) NOT NULL,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        cursor.execute("SELECT COUNT(*) FROM test_definitions")
        if cursor.fetchone()[0] == 0:
            fetchTestDefinitions(testType1)
            fetchTestDefinitions(testType2)
            fetchTestDefinitions(testType3)
            fetchTestDefinitions(testType4)

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS status_definitions (
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
            populateStatusDefinitions(1, "registered", 2, "Pending", 2, "specimen_accepted")
            populateStatusDefinitions(2, "Received", 3, "Started", 2, "specimen_accepted")
            populateStatusDefinitions(3, "registered", 3, "Started", 2, "specimen_accepted")
            populateStatusDefinitions(4, "registered", 4, "Completed", 2, "specimen_accepted")
            populateStatusDefinitions(5, "registered", 5, "Verified", 2, "specimen_accepted")

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER NOT NULL UNIQUE,
                accession_id INTEGER NOT NULL,
                test_type VARCHAR(100) NOT NULL,
                test_status VARCHAR(100) NOT NULL,
                write_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        cursor.execute('CREATE INDEX IF NOT EXISTS idx_accession_id ON tests(accession_id);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_type ON tests(test_type);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_status ON tests(test_status);')
        cursor.execute('CREATE INDEX IF NOT EXISTS idx_write_date ON tests(write_date);')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_summary (
                id INTEGER NOT NULL UNIQUE,
                weekly_registered INTEGER,
                weekly_received INTEGER,
                weekly_progress INTEGER,
                weekly_pending INTEGER,
                weekly_complete INTEGER,
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

        # to track every received
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allReceived (
                id INTEGER NOT NULL,
                accession_id VARCHAR(100) NOT NULL,
                test_type VARCHAR(100) NOT NULL,
                write_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id AUTOINCREMENT)
            )
        ''')


        # to track every inProgress
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allInProgress (
                id INTEGER NOT NULL,
                accession_id VARCHAR(100) NOT NULL,
                test_type VARCHAR(100) NOT NULL,
                write_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id AUTOINCREMENT)
            )
        ''')


        # to track every pendingAuth
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allPendingAuth (
                id INTEGER NOT NULL,
                accession_id VARCHAR(100) NOT NULL,
                test_type VARCHAR(100) NOT NULL,
                write_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id AUTOINCREMENT)
            )
        ''')


        # to track every completed
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS allCompleted (
                id INTEGER NOT NULL,
                accession_id VARCHAR(100) NOT NULL,
                test_type VARCHAR(100) NOT NULL,
                write_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY (id AUTOINCREMENT)
            )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()


# return department id
def getDepartmentId():
    try:
        conn = sqlite3.connect('models/intermediateDB.db')
        cursor = conn.cursor()
        query = 'SELECT department_id FROM department_definitions WHERE id = 1;'
        cursor.execute(query)
        result = cursor.fetchone()
        department_id = result[0] if result else 0
        return department_id
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None
    finally:
        if conn:
            conn.close()

# get the id to filter out the views

# check if the view already exists
def view_exists():
    try:
        cursor = mydb.cursor()
        query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.VIEWS WHERE TABLE_NAME = %s AND TABLE_SCHEMA = DATABASE();"
        cursor.execute(query, (screenName,))
        result = cursor.fetchone()
        cursor.close()
        return result is not None
    except mysql.connector.Error as e:
        print(f"Error connecting to MySQL database: {e}")
        return False

def createView():
    try:
        if not view_exists():
            cursor = mydb.cursor()
            query = (
            f'''
                CREATE VIEW {screenName} AS
                SELECT 
                    specimens.accession_number AS accession_id,
                    tests.test_type_id AS test_type,
                    tests.test_status_id AS test_status
                FROM 
                    specimens
                INNER JOIN 
                    tests ON specimens.id = tests.specimen_id
                WHERE 
                    specimens.specimen_type_id = {getDepartmentId()}
                    AND tests.test_status_id NOT IN (1, 5, 6, 7, 8)
                    AND tests.time_created >= NOW() - INTERVAL {interval} DAY
                    AND tests.test_type_id IN ({getTestTypeId(testType1)}, {getTestTypeId(testType2)}, {getTestTypeId(testType3)}, {getTestTypeId(testType4)});
            '''
            )
            cursor.execute(query)
            mydb.commit()
            cursor.close()
            return f"View {screenName} created successfully."
        else:
            return f"View {screenName} already exists."
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return False
    
def dropView():
    try:
        if view_exists():
            cursor = mydb.cursor()
            query = (
            f'''
                DROP view {screenName};
            '''
            )
            cursor.execute(query)
            mydb.commit()
            cursor.close()
            return f"View {screenName} created Dropped."
        else:
            return f"View {screenName} does not already exists."
    except mysql.connector.Error as e:
        print(f"Error connecting to database: {e}")
        return False
    

# dropView() run this at the start of the day
dbSetup() #run this at the installation
createView() #

# for tracking
"""
for sideBar summary:Recieved, test_type
for weekly Summary: Recieved (int)

"""