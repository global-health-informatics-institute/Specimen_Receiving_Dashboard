from config import iBlissDB, department, srsDB, testType1,testType2,testType3,testType4, Error
from helper import populateStatusDefinitionsHelper

def populateDepartmentDefinitions():
    iBlisCursor = None
    srsCursor = None
    iBlissConn = None
    srsConn = None

    try:
        iBlissConn = iBlissDB()
        if iBlissConn is None:
            print("Failed to connect to iBlissDB")
            return

        iBlisCursor = iBlissConn.cursor()
        iBlisCursor.execute(f"SELECT id FROM test_categories WHERE LCASE(name) = '{department.lower()}'")
        result = iBlisCursor.fetchone()

        if result:
            department_id = result[0]
            try:
                srsConn = srsDB()
                if srsConn is None:
                    print("Failed to connect to srsDB")
                    return

                srsCursor = srsConn.cursor()
                srsCursor.execute("SELECT COUNT(*) FROM department_definitions WHERE department_id = %s", (department_id,))
                count = srsCursor.fetchone()[0]

                if count == 0:
                    srsCursor.execute('''INSERT INTO department_definitions(department_id, department_name) 
                                         VALUES (%s, %s)''', (department_id, department))
                    srsConn.commit()
                else:
                    print("Entry already exists in department_definitions.")
            except Exception as e:
                print(f"Error inserting into department_definitions: {e}")
            finally:
                if srsCursor:
                    srsCursor.close()
                if srsConn:
                    srsConn.close()
    except Exception as e:
        print(f"Error fetching from test_categories: {e}")
    finally:
        if iBlisCursor:
            iBlisCursor.close()
        if iBlissConn:
            iBlissConn.close()
# populateDepartmentDefinitions()


def populateTestDefinitions():
    try:
        # Connect to iBlissDB
        iBlissConnection = iBlissDB()
        if iBlissConnection is None:
            print("Failed to connect to iBlissDB.")
            return
        
        iBlissCursor = iBlissConnection.cursor()
        
        # Connect to srsDB
        srsConnection = srsDB()
        if srsConnection is None:
            print("Failed to connect to srsDB.")
            return
        
        srsCursor = srsConnection.cursor()

        # List of test types
        test_types = [testType1, testType2, testType3, testType4]

        for testType in test_types:
            # Fetch test definitions from iBlissDB
            iBlissCursor.execute(f"SELECT id, name, short_name, targetTAT FROM test_types WHERE LCASE(short_name) = '{testType.lower()}'")
            result = iBlissCursor.fetchone()
            
            if result:
                test_id, name, short_name, targetTAT = result

                # Check if the entry already exists in srsDB
                srsCursor.execute(
                    "SELECT COUNT(*) FROM test_definitions WHERE test_id = %s OR test_short_name = %s",
                    (test_id, short_name)
                )
                count = srsCursor.fetchone()[0]

                if count == 0:
                    # Insert into test_definitions in srsDB if not exists
                    srsCursor.execute(
                        "INSERT INTO test_definitions (test_id, test_name, test_short_name, targetTAT) VALUES (%s, %s, %s, %s)",
                        (test_id, name, short_name, targetTAT)
                    )
                    srsConnection.commit()
                    print("Test definitions populated successfully.")
                else:
                    print("Already Populated")
    except Error as e:
        print(f"Error: {e}")
    finally:
        # Close cursors and connections
        if iBlissCursor:
            iBlissCursor.close()
        if iBlissConnection and iBlissConnection.is_connected():
            iBlissConnection.close()
        if srsCursor:
            srsCursor.close()
        if srsConnection and srsConnection.is_connected():
            srsConnection.close()
# populateTestDefinitions()


def populateStatusDefinitions():
    try:
        # Connect to srsDB
        srsConnection = srsDB()
        if srsConnection is None:
            print("Failed to connect to srsDB.")
            return
        
        srsCursor = srsConnection.cursor()

        # Check if the table is empty
        srsCursor.execute("SELECT COUNT(*) FROM status_definitions")
        count = srsCursor.fetchone()[0]

        if count == 0:
            # Populate the status_definitions table
            status_definitions = [
                (1, "registered", 2, "Pending", 2, "specimen_accepted"),
                (2, "Received", 3, "Started", 2, "specimen_accepted"),
                (3, "registered", 3, "Started", 2, "specimen_accepted"),
                (4, "registered", 4, "Completed", 2, "specimen_accepted"),
                (5, "registered", 5, "Verified", 2, "specimen_accepted")
            ]
            
            for status in status_definitions:
                populateStatusDefinitionsHelper(*status)

        print("Status definitions populated successfully.")

    except Error as e:
        print(f"Error: {e}")
    finally:
        if srsCursor:
            srsCursor.close()
        if srsConnection and srsConnection.is_connected():
            srsConnection.close()
# populateStatusDefinitions()

def populateReplicate(department):
    ""
    # iblis DB conn obj iBlissDB
    # join these tables as {department}
    # SELECT 
    #     specimens.accession_number AS accession_id,
    #     tests.test_type_id AS test_type,
    #     tests.test_status_id AS test_status
    # FROM
    # specimens
    # INNER JOIN 
    #     tests ON specimens.id = tests.specimen_id
    # WHERE 
    #     specimens.specimen_type_id = {getDepartmentId()}
    #     AND tests.test_status_id NOT IN (1, 6, 7, 8)
    #     AND tests.time_created >= NOW() - INTERVAL {interval} DAY
    #     AND tests.test_type_id IN ({getTestTypeId(testType1)}, {getTestTypeId(testType2)}, {getTestTypeId(testType3)}, {getTestTypeId(testType4)});