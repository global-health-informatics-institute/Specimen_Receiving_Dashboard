# department_id = getDepartmentIDHelper()
    # test_type_id1 = getTestTypeID(testType1)
    # test_type_id2 = getTestTypeID(testType2)
    # test_type_id3 = getTestTypeID(testType3)
    # test_type_id4 = getTestTypeID(testType4)

# def migrateAllUnique():
    # this will run at the begining of loading the db
    
    # weeklyIncrementorObj = WeeklyIncrementor()
    # monthlyIncrementorOnj = MonthlyIncrementor()
    # using the data from fetchFromJoin()
    # try srsDB obj
    # insert entry value into tests
        # but first, check if the entries fetched status test_status is not = 5
        # 5 means its already completed
            # check if the entry with the fetched accession_id is not already in the tests
            # if the entry does not already exist, then insert values
            # 'INSERT INTO tests in these columns(accession_id, test_type, test_status) the fetched values as (accession_id, test_type, test_status))
        # address all closing and exceptions


from config import srsDB, Error
from helper import fetchFromJoin
from monthlyData import MonthlyIncremator
from weeklyData import WeeklyIncremator


def migrateAllUnique():
    weeklyIncrementorObj = WeeklyIncremator()
    monthlyIncrementorObj = MonthlyIncremator()

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
                    INSERT INTO tests (accession_id, test_type_id, test_status)
                    VALUES (%s, %s, %s)
                    """
                    srsCursor.execute(insert_query, (accession_id, test_type_id, test_status))
                    srsConnection.commit()

                    if test_status == 2:
                        weeklyIncrementorObj.incrementRegistered()
                        monthlyIncrementorObj.incrementRegistered()
                    elif test_status == 3:
                        weeklyIncrementorObj.incrementInprogress()
                        monthlyIncrementorObj.incrementInprogress()
                    elif test_status == 4:
                        weeklyIncrementorObj.incrementPendingAuth()
                        monthlyIncrementorObj.incrementPendingAuth()

    except Error as e:
        print(f"Error: {e}")
    finally:
        if srsCursor:
            srsCursor.close()
        if srsConnection and srsConnection.is_connected():
            srsConnection.close()
        weeklyIncrementorObj.closeConnections()
        monthlyIncrementorObj.closeConnections()
migrateAllUnique()