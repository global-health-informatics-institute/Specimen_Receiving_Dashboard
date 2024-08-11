from mysql.connector import Error
from models.config import srsDBConn, srsDB, department


# create database
def createIntermediate():
    mydb = None
    cursor = None
    try:
        # Connect to MySQL server
        mydb = srsDBConn()
        
        # Create a cursor object
        cursor = mydb.cursor()
        
        # Check if the database exists
        cursor.execute(f"SHOW DATABASES LIKE '{department}'")
        database_exists = cursor.fetchone()
        
        if not database_exists:
            # Create the database if it doesn't exist
            cursor.execute(f"CREATE DATABASE {department}")
            print(f"Database '{department}' created successfully.")
        else:
            print(f"Database '{department}' already exists.")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if mydb is not None and mydb.is_connected():
            mydb.close()
createIntermediate()

# define the tables
def defineTables():
    try:
        # Connect to MySQL database
        conn = srsDB()

        if conn.is_connected():

            cursor = conn.cursor()

            # Create department_definitions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS department_definitions (
                    id INT NOT NULL UNIQUE DEFAULT 1 CHECK (id = 1),
                    department_id INT NOT NULL,
                    department_name VARCHAR(100) NOT NULL,  
                    PRIMARY KEY (id)
                )
            ''')

            # Create test_definitions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS test_definitions (
                    id INT NOT NULL AUTO_INCREMENT UNIQUE,
                    test_id INT NOT NULL,
                    test_name VARCHAR(100) NOT NULL,
                    test_short_name VARCHAR(100) NOT NULL,
                    targetTAT VARCHAR(100) NOT NULL,
                    PRIMARY KEY (id)
                )
            ''')

            # Create status_definitions table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS status_definitions (
                    id INT NOT NULL AUTO_INCREMENT UNIQUE,
                    status_id INT NOT NULL,
                    status_name VARCHAR(100) NOT NULL,
                    test_status_id INT NOT NULL,
                    test_status_name VARCHAR(100) NOT NULL,
                    specimen_status_id INT NOT NULL,
                    specimen_status_name VARCHAR(100) NOT NULL,
                    PRIMARY KEY (id)
                )
            ''')

            # Create tests table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS tests (
                    id INT NOT NULL AUTO_INCREMENT UNIQUE,
                    accession_id VARCHAR(100) NOT NULL,
                    test_type VARCHAR(100) NOT NULL,
                    test_status VARCHAR(100) NOT NULL,
                    write_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    PRIMARY KEY (id),
                    INDEX idx_accession_id (accession_id),
                    INDEX idx_test_type (test_type),
                    INDEX idx_test_status (test_status),
                    INDEX idx_write_date (write_date)
                )
            ''')

            # Create weekly_summary table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS weekly_summary (
                    id INT NOT NULL UNIQUE DEFAULT 1 CHECK (id = 1),
                    weekly_registered INT DEFAULT 0,
                    weekly_received INT DEFAULT 0,
                    weekly_progress INT DEFAULT 0,
                    weekly_pending INT DEFAULT 0,
                    weekly_complete INT DEFAULT 0,
                    weekly_rejected INT DEFAULT 0,
                    PRIMARY KEY (id),
                    INDEX idx_weekly_registered (weekly_registered),
                    INDEX idx_weekly_received (weekly_received),
                    INDEX idx_weekly_progress (weekly_progress),
                    INDEX idx_weekly_pending (weekly_pending),
                    INDEX idx_weekly_complete (weekly_complete),
                    INDEX idx_weekly_rejected (weekly_rejected)
                )
            ''')

            # Create monthly_summary table
            cursor.execute('''
                CREATE TABLE IF NOT EXISTS monthly_summary (
                    id INT NOT NULL UNIQUE DEFAULT 1 CHECK (id = 1),
                    monthly_registered INT DEFAULT 0,
                    monthly_received INT DEFAULT 0,
                    monthly_progress INT DEFAULT 0,
                    monthly_pending INT DEFAULT 0,
                    monthly_complete INT DEFAULT 0,
                    monthly_rejected INT DEFAULT 0,
                    PRIMARY KEY (id),
                    INDEX idx_monthly_registered (monthly_registered),
                    INDEX idx_monthly_received (monthly_received),
                    INDEX idx_monthly_progress (monthly_progress),
                    INDEX idx_monthly_pending (monthly_pending),
                    INDEX idx_monthly_complete (monthly_complete),
                    INDEX idx_monthly_rejected (monthly_rejected)
                )
            ''')

            conn.commit()

    except Error as e:
        print(f"Error: {e}")
defineTables()
