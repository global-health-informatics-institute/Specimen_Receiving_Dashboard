import mysql.connector
from mysql.connector import Error

# create database
def createIntermediate():
    mydb = None
    cursor = None
    try:
        # Connect to MySQL server
        mydb = mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="root"
        )
        
        # Create a cursor object
        cursor = mydb.cursor()
        
        # Check if the database exists
        cursor.execute("SHOW DATABASES LIKE 'intermediate'")
        database_exists = cursor.fetchone()
        
        if not database_exists:
            # Create the database if it doesn't exist
            cursor.execute("CREATE DATABASE intermediate")
            print("Database 'intermediate' created successfully.")
        else:
            print("Database 'intermediate' already exists.")
        
    except Error as e:
        print(f"Error: {e}")
    finally:
        if cursor is not None:
            cursor.close()
        if mydb is not None and mydb.is_connected():
            mydb.close()

createIntermediate()

# create THE VIEW

# define the tables
    # department_definitions
    # status_definitions
    # test_definitions
    # test
    # monthly_summary
    # weekly_summary
# create Indecies
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_accession_id ON tests(accession_id);')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_type ON tests(test_type);')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_test_status ON tests(test_status);')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_write_date ON tests(write_date);')

    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_weekly_registered ON weekly_summary (weekly_registered)')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_weekly_received ON weekly_summary (weekly_received)')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_weekly_progress ON weekly_summary (weekly_progress)')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_weekly_pending ON weekly_summary (weekly_pending)')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_weekly_complete ON weekly_summary (weekly_complete)')

    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_monthly_registered ON monthly_summary (monthly_registered)')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_monthly_received ON monthly_summary (monthly_received)')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_monthly_progress ON monthly_summary (monthly_progress)')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_monthly_pending ON monthly_summary (monthly_pending)')
    # cursor.execute('CREATE INDEX IF NOT EXISTS idx_monthly_complete ON monthly_summary (monthly_complete)')

