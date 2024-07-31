from models.config import iBlissDB, srsDB, Error, department, testType1, testType2, testType3, testType4, interval


def populateStatusDefinitionsHelper(statusId, statusName, testStatusId, testStatusName, specimenStatusId, specimenStatusName):
    try:
        srsConnection = srsDB()
        if srsConnection is None:
            print("Failed to connect to srsDB.")
            return
        
        srsCursor = srsConnection.cursor()
        
        srsCursor.execute(
            "INSERT INTO status_definitions (status_id, status_name, test_status_id, test_status_name, specimen_status_id, specimen_status_name) VALUES (%s, %s, %s, %s, %s, %s)",
            (statusId, statusName, testStatusId, testStatusName, specimenStatusId, specimenStatusName)
        )
        srsConnection.commit()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if srsCursor:
            srsCursor.close()
        if srsConnection and srsConnection.is_connected():
            srsConnection.close()

            
def getDepartmentIdHelper():
    try:
        # Connect to srsDB
        srsConnection = srsDB()
        if srsConnection is None:
            print("Failed to connect to srsDB.")
            return None
        
        srsCursor = srsConnection.cursor()

        # Query to get the department_id for the specified department
        srsCursor.execute("SELECT department_id FROM department_definitions WHERE department_name = %s", (department,))
        result = srsCursor.fetchone()

        if result:
            department_id = result[0]
            return department_id
        else:
            print(f"No department found with the name '{department}'.")
            return None
    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if srsCursor:
            srsCursor.close()
        if srsConnection and srsConnection.is_connected():
            srsConnection.close()
# used when creating the join
# print(getDepartmentIdHelper())

def getTestTypeID(testType):
    try:
        # Connect to srsDB
        srsConnection = srsDB()
        if srsConnection is None:
            print("Failed to connect to srsDB.")
            return None
        
        srsCursor = srsConnection.cursor()

        # Query to get the test_type_id for the specified test_short_name
        srsCursor.execute("SELECT test_id FROM test_definitions WHERE lcase(test_short_name) = %s", (testType.lower(),))
        result = srsCursor.fetchone()

        if result:
            test_type_id = result[0]
            return test_type_id
        else:
            print(f"No test type found with the short name '{testType}'.")
            return None

    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if srsCursor:
            srsCursor.close()
        if srsConnection and srsConnection.is_connected():
            srsConnection.close()
# used when create the join


def fetchFromJoin():
    try:
        # Connect to iBlissDB
        iblisConnection = iBlissDB()
        if iblisConnection is None:
            print("Failed to connect to iBlissDB.")
            return None
        
        iblisCursor = iblisConnection.cursor()

        # Get the department ID and test type IDs
        department_id = getDepartmentIdHelper()
        test_type_id1 = getTestTypeID(testType1)
        test_type_id2 = getTestTypeID(testType2)
        test_type_id3 = getTestTypeID(testType3)
        test_type_id4 = getTestTypeID(testType4)

        if None in (department_id, test_type_id1, test_type_id2, test_type_id3, test_type_id4):
            print("One or more required IDs could not be fetched.")
            return None

        # Query to fetch data from the join
        query = f"""
        SELECT 
            specimens.accession_number AS accession_id,
            tests.test_type_id AS test_type,
            tests.test_status_id AS test_status
        FROM 
            specimens
        INNER JOIN 
            tests ON specimens.id = tests.specimen_id
        WHERE 
            specimens.specimen_type_id = %s
            AND tests.test_status_id NOT IN (1, 6, 7, 8)
            AND tests.time_created >= NOW() - INTERVAL %s DAY
            AND tests.test_type_id IN (%s, %s, %s, %s)
        """

        iblisCursor.execute(query, (department_id, interval, test_type_id1, test_type_id2, test_type_id3, test_type_id4))
        results = iblisCursor.fetchall()

        formattedResults = [
            {
                "accession_id": row[0],
                "test_type_id": row[1],
                "test_status": row[2]
            }
            for row in results
        ]

        return formattedResults

    except Error as e:
        print(f"Error: {e}")
        return None
    finally:
        if iblisCursor:
            iblisCursor.close()
        if iblisConnection and iblisConnection.is_connected():
            iblisConnection.close()

# print(fetchFromJoin())
