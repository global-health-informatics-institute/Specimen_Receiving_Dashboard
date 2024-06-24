import mysql.connector
from models.helper import getDepartmentIdHelper, getTestTypeID
from models.config import testType1, testType2, testType3, testType4, interval

intvl = interval  # 100
department_id = getDepartmentIdHelper()  # 3
test_type_id1 = getTestTypeID(testType1)  # 35
test_type_id2 = getTestTypeID(testType2)  # 39
test_type_id3 = getTestTypeID(testType3)  # 40
test_type_id4 = getTestTypeID(testType4)  # 41

# i want to keep track of each status as per week and monthly
def _updateFieldHelperWeekly(status):
    if status == 2:
        column_name = "weekly_registered"
    elif status == 0:
        column_name = "weekly_received"
    elif status == 3:
        column_name = "weekly_progress"
    elif status == 4:
        column_name = "weekly_pending"
    elif status == 5:
        column_name = "weekly_complete"

    query = f"UPDATE weekly_summary SET {column_name} = {column_name} + 1 WHERE id = 1;"
    return query

def _updateFieldHelperMonthly(status):
    if status == 2:
        column_name = "monthly_registered"
    elif status == 0:
        column_name = "monthly_received"
    elif status == 3:
        column_name = "monthly_progress"
    elif status == 4:
        column_name = "monthly_pending"
    elif status == 5:
        column_name = "monthly_complete"
        
    query = f"UPDATE monthly_summary SET {column_name} = {column_name} + 1 WHERE id = 1;"
    return query

def loadEntries():
    try:
        # Connect to iBlissDB
        with mysql.connector.connect(
            host="127.0.0.1",
            port="3306",
            user="root",
            password="root",
            database="tests"
        ) as iblis_connection:
            # Connect to srsDB
            with mysql.connector.connect(
                host="127.0.0.1",
                port="3306",
                user="root",
                password="root",
                database="Haematology"
            ) as srs_connection:

                iblis_cursor = iblis_connection.cursor(dictionary=True)
                srs_cursor = srs_connection.cursor(dictionary=True)

                # iblis_query to fetch the required data
                iblis_query = """
                WITH RankedTests AS (
                    SELECT 
                        specimens.accession_number AS accession_id,
                        tests.test_type_id AS test_type,
                        tests.test_status_id AS test_status,
                        ROW_NUMBER() OVER (
                            PARTITION BY specimens.accession_number, tests.test_type_id 
                            ORDER BY tests.time_created DESC
                        ) AS rn
                    FROM 
                        specimens
                    INNER JOIN 
                        tests ON specimens.id = tests.specimen_id
                    WHERE 
                        specimens.specimen_type_id = %s
                        AND tests.test_status_id NOT IN (1, 6, 7, 8)
                        AND tests.time_created >= CURDATE() + INTERVAL 7 HOUR
                        AND tests.time_created <= CURDATE() + INTERVAL 1 DAY + INTERVAL 7 HOUR 
                        AND tests.test_type_id IN (%s, %s, %s, %s)
                )
                SELECT
                    accession_id,
                    test_type,
                    test_status
                FROM
                    RankedTests
                WHERE
                    rn = 1;
                """

                # Execute the query
                iblis_cursor.execute(iblis_query, (department_id, test_type_id1, test_type_id2, test_type_id3, test_type_id4))
                iblis_results = iblis_cursor.fetchall()

                # Insert the results into srsDB if they don't already exist
                for result in iblis_results:
                    accession_id = result['accession_id']
                    test_type = result['test_type']
                    test_status = result['test_status']

                    # Check if accession_id with the same test_type already exists in the srsDB tests table
                    srs_cursor.execute("SELECT test_status FROM tests WHERE accession_id = %s AND test_type = %s", (accession_id, test_type))
                    existing_record = srs_cursor.fetchone()

                    # condition 1: insert if the entry does not exist and status is not 5 (5 means it's completed already)
                    if not existing_record:
                        # Insert the record into srsDB
                        srs_insert_query = """
                        INSERT INTO tests (accession_id, test_type, test_status)
                        VALUES (%s, %s, %s)
                        """
                        srs_cursor.execute(_updateFieldHelperWeekly(test_status))
                        srs_cursor.execute(_updateFieldHelperMonthly(test_status))
                        srs_cursor.execute(srs_insert_query, (accession_id, test_type, test_status))
                        srs_connection.commit()
                        print(f"Inserted new record for accession_id: {accession_id}, test_type: {test_type}, test_status: {test_status}")

                    else:
                        existing_status = int(existing_record['test_status'])  # Convert to int
                        print(f"Comparing new test_status: {test_status} (type: {type(test_status)}) with old test_status: {existing_status} (type: {type(existing_status)})")

                        if existing_status == test_status:
                            print(f"No update needed for accession_id: {accession_id}, test_type: {test_type}, test_status: {test_status}")
                            continue

                        # condition 2: skip if the existing status = 0 and new entry is either 1, 2
                        elif existing_status == 0 and test_status in [1, 2]:
                            continue

                        else:
                            # condition 3: Update the status if it is different
                            srs_update_query = """
                            UPDATE tests
                            SET test_status = %s
                            WHERE accession_id = %s AND test_type = %s
                            """
                            srs_cursor.execute(srs_update_query, (test_status, accession_id, test_type))
                            srs_cursor.execute(_updateFieldHelperWeekly(test_status))
                            srs_cursor.execute(_updateFieldHelperMonthly(test_status))
                            srs_connection.commit()
                            print(f"Updated record for accession_id: {accession_id}, test_type: {test_type}, new test_status: {test_status}, old test_status: {existing_status}")
        return "ok"

    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return "Error occurred while updating entries"

    finally:
        # Close all connections and cursors
        if 'iblis_cursor' in locals() and iblis_cursor:
            iblis_cursor.close()
        if 'srs_cursor' in locals() and srs_cursor:
            srs_cursor.close()


