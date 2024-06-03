from config import *
import sqlite3

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
                    AND tests.test_status_id NOT IN (1, 6, 7, 8)
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

