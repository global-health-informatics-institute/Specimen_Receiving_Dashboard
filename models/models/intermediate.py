from config import srsDB, Error
from helper import fetchFromJoin
from monthlyData import MonthlyIncremator
from weeklyData import WeeklyIncremator

def _updateFieldHelper(connectionObj, cursorObj, table, column_name):
    try:
        if cursorObj:
            query = f"UPDATE {table} SET {column_name} = {column_name} + 1 WHERE id = 1;"
            cursorObj.execute(query)
            connectionObj.commit()  # Commit the transaction to save changes
        else:
            print("Cursor not initialized.")
    except Error as e:
        print(f"Error: {e}")

def migrateAllUnique():
    try:
        srsConnection = srsDB()
        if srsConnection is None:
            print("Failed to connect to srsDB.")
            return
        
        srsCursor = srsConnection.cursor()

        fetched_data = fetchFromJoin()
        if fetched_data is None:
            print("Failed to fetch data from join.")
            return

        for entry in fetched_data:
            accession_id = entry["accession_id"]
            test_type_id = entry["test_type_id"]
            test_status = entry["test_status"]

            if test_status != 5:
                srsCursor.execute("SELECT COUNT(*) FROM tests WHERE accession_id = %s", (accession_id,))
                exists = srsCursor.fetchone()[0]

                if not exists:
                    insert_query = """
                    INSERT INTO tests (accession_id, test_type, test_status)
                    VALUES (%s, %s, %s)
                    """
                    if test_status == 2:
                        print("2")
                        _updateFieldHelper(srsConnection, srsCursor, 'weekly_summary', 'weekly_registered')
                        _updateFieldHelper(srsConnection, srsCursor, 'monthly_summary', 'monthly_registered')
                    elif test_status == 3:
                        print("not 2")
                        _updateFieldHelper(srsConnection, srsCursor, 'weekly_summary', 'weekly_progress')
                        _updateFieldHelper(srsConnection, srsCursor, 'monthly_summary', 'monthly_progress')
                    elif test_status == 4:
                        print("not 2,3")
                        _updateFieldHelper(srsConnection, srsCursor, 'weekly_summary', 'weekly_pending')
                        _updateFieldHelper(srsConnection, srsCursor, 'monthly_summary', 'monthly_pending')

                    srsCursor.execute(insert_query, (accession_id, test_type_id, test_status))
                    srsConnection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if srsCursor:
            srsCursor.close()
        if srsConnection:
            srsConnection.close()

migrateAllUnique()
