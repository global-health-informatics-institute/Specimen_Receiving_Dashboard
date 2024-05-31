import sqlite3

class TestsData:
    def __init__(self, testType):
        self.connection = sqlite3.connect('models/intermediateDB.db')
        self.cursor = self.connection.cursor()
        self.testType = testType

    def getRegistered(self):
        """Get the total count of tests with status 'registered'."""
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE LOWER(test_status) = "registered" AND LOWER(test_type) = ?;'
        self.cursor.execute(query, (self.testType.lower(),))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status

    def getReceived(self):
        """Get the total count of tests with status 'received'."""
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE LOWER(test_status) = "received" AND LOWER(test_type) = ?;'
        self.cursor.execute(query, (self.testType.lower(),))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status

    def getInProgress(self):
        """Get the total count of tests with status 'in_progress'."""
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE LOWER(test_status) = "in_progress" AND LOWER(test_type) = ?;'
        self.cursor.execute(query, (self.testType.lower(),))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status

    def getPendingAuth(self):
        """Get the total count of tests with status 'pending_auth'."""
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE LOWER(test_status) = "pending_auth" AND LOWER(test_type) = ?;'
        self.cursor.execute(query, (self.testType.lower(),))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status

    def getComplete(self):
        """Get the total count of tests with status 'complete'."""
        query = 'SELECT COUNT(id) AS totalStatus FROM tests WHERE LOWER(test_status) = "complete" AND LOWER(test_type) = ?;'
        self.cursor.execute(query, (self.testType.lower(),))
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status

    def closeConn(self):
        """Close the database connection."""
        self.cursor.close()
        self.connection.close()
