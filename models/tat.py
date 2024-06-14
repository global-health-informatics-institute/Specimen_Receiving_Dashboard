import sqlite3

class TATData:
    def __init__(self, testType):
        self.connection = None
        self.cursor = None
        self.testType = testType
        self._connect()

    def _connect(self):
        """Establish a database connection and create a cursor."""
        try:
            self.connection = sqlite3.connect('models/intermediateDB.db')
            self.cursor = self.connection.cursor()
        except sqlite3.Error as e:
            print(f"Error connecting to database: {e}")

    def targetTAT(self):
        """Get the total count of tests with status 'registered'."""
        if not self.cursor:
            print("Database connection not established.")
            return None
        # srsDB obj
        # query = 'SELECT targetTAT FROM test_definitions WHERE LOWER(test_short_name) = ?;'
        # return results its a string
        
        query = 'SELECT targetTAT FROM test_definitions WHERE LOWER(test_short_name) = ?;'
        try:
            self.cursor.execute(query, (self.testType.lower(),))
            result = self.cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error executing query: {e}")
            return None

    def close(self):
        """Close the database connection."""
        if self.connection:
            self.connection.close()

    
    def getCurrent(self):
        ""

    def getAverage(self):
        ""