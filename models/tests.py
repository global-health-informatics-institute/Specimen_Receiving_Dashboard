from models.config import srsDB, Error, interval, time_out
from models.helper import getTestTypeID

def testTypeId(testType):
    test_type_id = getTestTypeID(testType)  
    return test_type_id

class TestsData:
    def __init__(self, test_type):
        self.test_type = testTypeId(test_type)
        self.srsDB = srsDB()
        if self.srsDB is None:
            print("Failed to connect to srsDB.")
        else:
            self.srsCursor = self.srsDB.cursor()

    def _getTestCount(self, query):
        try:
            if self.srsCursor:
                self.srsCursor.execute(query)
                result = self.srsCursor.fetchone()
                return result[0] if result else 0
            else:
                print("Cursor not initialized.")
                return 0
        except Exception as e:
            print(f"Error: {e}")
            return 0 
        
    def getReceived(self):
        query = f"""
            SELECT COUNT(id) AS totalStatus
                FROM tests
                WHERE write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {interval} HOUR
                AND test_status = 0
                AND test_type = '{self.test_type}';
            """
        return self._getTestCount(query)
        
    def getInProgress(self):
        query = f"""
            SELECT COUNT(id) AS totalStatus
                FROM tests
                WHERE write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR
                AND test_status = 3
                AND test_type = '{self.test_type}';
            """
        return self._getTestCount(query)
            
    def getPendingAuth(self):
        query = f"""
            SELECT COUNT(id) AS totalStatus
                FROM tests
                WHERE write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR
                AND test_status = 4
                AND test_type = '{self.test_type}';
            """
        return self._getTestCount(query)
    
    def getComplete(self):
        query = f"""
            SELECT COUNT(id) AS totalStatus
                FROM tests
                WHERE write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR
                AND test_status = 5
                AND test_type = '{self.test_type}';
            """
        return self._getTestCount(query)

    def getRegistered(self):
        # Assuming there's a method to get registered tests, implement accordingly
        query = f"""
            SELECT COUNT(id) AS totalStatus
                FROM tests
                WHERE write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR
                AND test_status != 9
                AND test_type = '{self.test_type}';
            """
        return self._getTestCount(query)

    def closeConn(self):
        try:
            if self.srsCursor:
                self.srsCursor.close()
            if self.srsDB and self.srsDB.is_connected():
                self.srsDB.close()
        except Error as e:
            print(f"Error closing connection: {e}")

    def getRejected(self):
        query = f"""
            SELECT COUNT(id) AS totalStatus
                FROM tests
                WHERE write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR
                AND test_status = 9
                AND test_type = '{self.test_type}';
            """
        return self._getTestCount(query)

# print(TestsData("APTT").getComplete())
# print(testTypeId("APTT"))
