import sqlite3

department = "Hematology"
testType1 = "FCB"
testType2 = "Sickle"
testType3 = "BloodSick"
testType4 = "Blue bloods"
def dbSetup():
    try:
        # DB connection
        conn = sqlite3.connect('models/intermediateDB.db')

        # cursor Object
        cursor = conn.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER NOT NULL UNIQUE,
                assertion_id INTEGER NOT NULL,
                department VARCHAR(100) NOT NULL,
                test_type VARCHAR(100) NOT NULL,
                test_status VARCHAR(100) NOT NULL,
                write_date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS weekly_summary (
                id INTEGER NOT NULL UNIQUE,
                weekly_registered INTEGER NOT NULL,
                weekly_received INTEGER NOT NULL,
                weekly_progress INTEGER NOT NULL,
                weekly_pending INTEGER NOT NULL,
                weekly_complete INTEGER NOT NULL,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS monthly_summary (
                id INTEGER NOT NULL UNIQUE,
                monthly_registered INTEGER NOT NULL,
                monthly_received INTEGER NOT NULL,
                monthly_progress INTEGER NOT NULL,
                monthly_pending INTEGER NOT NULL,
                monthly_complete INTEGER NOT NULL,
                PRIMARY KEY(id AUTOINCREMENT)
            )
        ''')

        conn.commit()
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
    finally:
        if conn:
            conn.close()
