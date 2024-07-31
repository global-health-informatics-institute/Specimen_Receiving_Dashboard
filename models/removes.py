import mysql.connector
from models.helper import getDepartmentIdHelper, getTestTypeID
from models.config import testType1, testType2, testType3, testType4, interval, iBlissDB, srsDB,time_out

intvl = interval  # 100
department_id = getDepartmentIdHelper()  # 3
test_type_id1 = getTestTypeID(testType1)  # 35
test_type_id2 = getTestTypeID(testType2)  # 39
test_type_id3 = getTestTypeID(testType3)  # 40
test_type_id4 = getTestTypeID(testType4)  # 41

def _updateFieldHelperWeekly(status):
    if status == 2:
        return "UPDATE weekly_summary SET weekly_registered = weekly_registered - 1 WHERE id = 1;"
    elif status == 0:
        return """
            UPDATE weekly_summary SET weekly_received = weekly_received - 1, 
            weekly_registered = weekly_registered - 1 WHERE id = 1;
        """
    elif status == 3:
        return """
            UPDATE weekly_summary SET weekly_progress = weekly_progress - 1, 
            weekly_received = weekly_received - 1, 
            weekly_registered = weekly_registered - 1 WHERE id = 1;
        """
    elif status == 4:
        return """
            UPDATE weekly_summary SET weekly_progress = weekly_progress - 1, 
            weekly_received = weekly_received - 1, 
            weekly_registered = weekly_registered - 1, 
            weekly_pending = weekly_pending - 1 WHERE id = 1;
        """
    elif status == 5:
        return """
            UPDATE weekly_summary SET weekly_progress = weekly_progress - 1, 
            weekly_received = weekly_received - 1, 
            weekly_registered = weekly_registered - 1, 
            weekly_pending = weekly_pending - 1, 
            weekly_complete = weekly_complete - 1 WHERE id = 1;
        """
    return ""

def _updateFieldHelperMonthly(status):
    if status == 2:
        return "UPDATE monthly_summary SET monthly_registered = monthly_registered - 1 WHERE id = 1;"
    elif status == 0:
        return """
            UPDATE monthly_summary SET monthly_received = monthly_received - 1, 
            monthly_registered = monthly_registered - 1 WHERE id = 1;
        """
    elif status == 3:
        return """
            UPDATE monthly_summary SET monthly_progress = monthly_progress - 1, 
            monthly_received = monthly_received - 1, 
            monthly_registered = monthly_registered - 1 WHERE id = 1;
        """
    elif status == 4:
        return """
            UPDATE monthly_summary SET monthly_progress = monthly_progress - 1, 
            monthly_received = monthly_received - 1, 
            monthly_registered = monthly_registered - 1, 
            monthly_pending = monthly_pending - 1 WHERE id = 1;
        """
    elif status == 5:
        return """
            UPDATE monthly_summary SET monthly_progress = monthly_progress - 1, 
            monthly_received = monthly_received - 1, 
            monthly_registered = monthly_registered - 1, 
            monthly_pending = monthly_pending - 1, 
            monthly_complete = monthly_complete - 1 WHERE id = 1;
        """
    return ""

def unLoadEntries():
    try:
        # Connect to iBlissDB
        iBlissConnection = iBlissDB()
        if iBlissConnection is None:
            print("Failed to connect to iBlissDB")
            return
        try:
            # Connect to srsDB
            srsConnection = srsDB()
            if srsConnection is None:
                print("Failed to connect to srsDB")
                return
            try:
                iblis_cursor = iBlissConnection.cursor(dictionary=True)
                srs_cursor = srsConnection.cursor(dictionary=True)

                # iblis_query to fetch the required data
                iblis_query = f"""
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
                        specimens.time_accepted IS NOT NULL
                        AND specimens.specimen_type_id = %s
                        AND tests.test_status_id IN (1, 6, 7, 8)
                        AND tests.time_created >= CURDATE() + INTERVAL {time_out} HOUR
                        AND tests.time_created <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR 
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

                iblis_cursor.execute(iblis_query, (department_id, test_type_id1, test_type_id2, test_type_id3, test_type_id4))
                iblis_results = iblis_cursor.fetchall()

                for result in iblis_results:
                    accession_id = result['accession_id']
                    test_type = result['test_type']

                    # Check if accession_id with the same test_type already exists in the srsDB tests table
                    srs_cursor.execute(
                        f"""
                        SELECT
                            accession_id,
                            test_type,
                            test_status as currentStatus
                        FROM
                            tests
                        WHERE
                            accession_id = %s
                            AND test_type = %s
                            AND write_date >= CURDATE() + INTERVAL {time_out} HOUR
                            AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR 
                        """, (accession_id, test_type))
                    existing_record = srs_cursor.fetchone()

                    if existing_record:
                        # Delete the existing record and update summaries
                        current_status = int(existing_record["currentStatus"])
                        srs_delete_query = f"""
                        DELETE FROM tests 
                        WHERE accession_id = %s 
                        AND test_type = %s 
                        AND write_date >= CURDATE() + INTERVAL {time_out} HOUR 
                        AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR;
                        """
                        srs_cursor.execute(srs_delete_query, (accession_id, test_type))
                        srs_cursor.execute(_updateFieldHelperWeekly(current_status))
                        srs_cursor.execute(_updateFieldHelperMonthly(current_status))
                        srsConnection.commit()
                        print(f"Deleted the record for accession_id: {accession_id}, test_type: {test_type}, test_status: {current_status}")
                    else:
                        continue
            finally:
                if srsConnection and srsConnection.is_connected():
                    srsConnection.close()
        finally:
            if iBlissConnection and iBlissConnection.is_connected():
                iBlissConnection.close()
                print("models.remove:green")
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
# unLoadEntries()