import sqlite3
from models.config import getTestTypeId

class TestsData:
    def __init__(self, testType):
        self.connection = sqlite3.connect('models/intermediateDB.db')
        self.cursor = self.connection.cursor()
        self.testType = testType

        
    def getRegistered(self):
            """Get the total count of tests with status 'registered'."""
            testTypeId = getTestTypeId(self.testType)
            if testTypeId is None:
                return 0

            query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE test_type = ?;'
            self.cursor.execute(query, (testTypeId,))
            result = self.cursor.fetchone()
            total_status = result[0] if result else 0
            return total_status

    def getReceived(self):
        """Get the total count of tests with status 'received'."""
        # query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE LOWER(test_status) = "received" AND LOWER(test_type) = ?;'
        # self.cursor.execute(query, (self.testType.lower(),))
        # result = self.cursor.fetchone()
        # total_status = result[0] if result else 0
        # return total_status
        # totalStatus = TestsData.getInProgress(self) + TestsData.getPendingAuth(self) + TestsData.getComplete(self)
        # return totalStatus
        testTypeId = getTestTypeId(self.testType)
        if testTypeId is None:
            return 0
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE test_type = ? AND test_status = 0;'
        self.cursor.execute(query, (testTypeId,))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status

    def getInProgress(self):
        """Get the total count of tests with status 'in_progress'."""
        testTypeId = getTestTypeId(self.testType)
        if testTypeId is None:
            return 0
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE test_type = ? AND test_status = 3;'
        self.cursor.execute(query, (testTypeId,))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status

    def getPendingAuth(self):
        """Get the total count of tests with status 'pending_auth'."""
        testTypeId = getTestTypeId(self.testType)
        if testTypeId is None:
            return 0
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE test_type = ? AND test_status = 4;'
        self.cursor.execute(query, (testTypeId,))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status

    def getComplete(self):
        testTypeId = getTestTypeId(self.testType)
        if testTypeId is None:
            return 0
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE test_type = ? AND test_status = 5;'
        self.cursor.execute(query, (testTypeId,))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status


    def closeConn(self):
        """Close the database connection."""
        self.cursor.close()
        self.connection.close()

