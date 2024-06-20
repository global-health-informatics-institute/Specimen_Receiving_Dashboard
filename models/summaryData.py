from config import srsDB, Error
from datetime import datetime

class SummaryData:
    def __init__(self):
        self.srsDB = srsDB()
        if self.srsDB is None:
            print("Failed to connect to srsDB.")
        else:
            self.srsCursor = self.srsDB.cursor()

    def _getSummaryCount(self, query):
        try:
            if self.srsCursor:
                self.srsCursor.execute(query)
                result = self.srsCursor.fetchone()
                return result[0] if result else 0
            else:
                print("Cursor not initialized.")
                return 0
        except Error as e:
            print(f"Error: {e}")
            return 0

    def getSummaryRegistered(self):
        query = "SELECT COUNT(id) AS totalStatus FROM tests WHERE DATE(write_date) = CURDATE();"
        return self._getSummaryCount(query)

    def getSummaryReceived(self):
        query = "SELECT COUNT(id) AS totalStatus FROM tests WHERE test_status = 0 AND DATE(write_date) = CURDATE();"
        return self._getSummaryCount(query)

    def getSummaryInprogress(self):
        query = "SELECT COUNT(id) AS totalStatus FROM tests WHERE test_status = 3 AND DATE(write_date) = CURDATE();"
        return self._getSummaryCount(query)

    def getSummaryPendingAuth(self):
        query = "SELECT COUNT(id) AS totalStatus FROM tests WHERE test_status = 4 AND DATE(write_date) = CURDATE();"
        return self._getSummaryCount(query)

    def getSummaryComplete(self):
        query = "SELECT COUNT(id) AS totalStatus FROM tests WHERE test_status = 5 AND DATE(write_date) = CURDATE();"
        return self._getSummaryCount(query)

    def closeConnections(self):
        try:
            if self.srsCursor:
                self.srsCursor.close()
            if self.srsDB and self.srsDB.is_connected():
                self.srsDB.close()
        except Error as e:
            print(f"Error closing connection: {e}")

# Example usage:
# summary_data = SummaryData()
# print(summary_data.getSummaryRegistered())
# print(summary_data.getSummaryReceived())
# print(summary_data.getSummaryInprogress())
# print(summary_data.getSummaryPendingAuth())
# print(summary_data.getSummaryComplete())
# summary_data.closeConnections()
