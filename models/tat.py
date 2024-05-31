import sqlite3

class TATData:
    def __init__(self, testType):
        self.connection = sqlite3.connect('models/intermediateDB.db')
        self.cursor = self.connection.cursor()
        self.testType = testType

    def targetTAT(self):
        """Get the total count of tests with status 'registered'."""
        query = 'SELECT targetTAT FROM test_definitions WHERE LOWER(test_short_name) = ?;'
        self.cursor.execute(query, (self.testType.lower(),))
        result = self.cursor.fetchone()
        return result
    
    def getCurrent(self):
        ""

    def getAverage(self):
        ""