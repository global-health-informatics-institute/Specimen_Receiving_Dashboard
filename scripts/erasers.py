import sqlite3

def clearTable(tableName):
    # Connect to the SQLite database
    conn = sqlite3.connect('models/intermediateDB.db')
    cursor = conn.cursor()
    try:
        # Execute the SQL command to delete all records from the 'tests' table
        cursor.execute(f"DELETE FROM {tableName}")
        conn.commit()  # Commit the transaction
        print("All records have been deleted from the 'tests' table.")
    except sqlite3.Error as e:
        print(f"An error occurred: {e}")
        conn.rollback()  # Rollback the transaction in case of error
    finally:
        # Close the cursor and the connection
        cursor.close()
        conn.close()
