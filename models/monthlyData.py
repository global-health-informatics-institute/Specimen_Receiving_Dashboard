from models.config import srsDB, Error

class MonthlyCounter:
    def __init__(self):
        self.srsDB = srsDB()
        if self.srsDB is None:
            print("Failed to connect to srsDB.")
        else:
            self.srsCursor = self.srsDB.cursor()

    def _getSummaryValueHelper(self, column_name):
        try:
            if self.srsCursor:
                query = f"SELECT {column_name} FROM monthly_summary WHERE id = 1"
                self.srsCursor.execute(query)
                result = self.srsCursor.fetchone()
                return int(result[0]) if result else 0
            else:
                print("Cursor not initialized.")
                return 0
        except Error as e:
            print(f"Error: {e}")
            return 0

    def getSummaryRegistered(self):
        return self._getSummaryValueHelper('monthly_registered')

    def getSummaryReceived(self):
        return self._getSummaryValueHelper('monthly_received')

    def getSummaryInprogress(self):
        return self._getSummaryValueHelper('monthly_progress')

    def getSummaryPendingAuth(self):
        return self._getSummaryValueHelper('monthly_pending')

    def getSummaryComplete(self):
        return self._getSummaryValueHelper('monthly_complete')

    def closeConnections(self):
        try:
            if self.srsCursor:
                self.srsCursor.close()
            if self.srsDB and self.srsDB.is_connected():
                self.srsDB.close()
        except Error as e:
            print(f"Error closing connection: {e}")


class MonthlyIncremator:
    def __init__(self):
        self.srsDB = srsDB()
        if self.srsDB is None:
            print("Failed to connect to srsDB.")
        else:
            self.srsCursor = self.srsDB.cursor()

    def _updateFieldHelper(self, column_name):
        try:
            if self.srsCursor:
                query = f"UPDATE monthly_summary SET {column_name} = {column_name} + 1 WHERE id = 1;"
                self.srsCursor.execute(query)
                self.srsDB.commit()  # Commit the transaction to save changes
            else:
                print("Cursor not initialized.")
        except Error as e:
            print(f"Error: {e}")

    def incrementRegistered(self):
        self._updateFieldHelper('monthly_registered')

    def incrementReceived(self):
        self._updateFieldHelper('monthly_received')

    def incrementInprogress(self):
        self._updateFieldHelper('monthly_progress')

    def incrementPendingAuth(self):
        self._updateFieldHelper('monthly_pending')

    def incrementComplete(self):
        self._updateFieldHelper('monthly_complete')

    def closeConnections(self):
        try:
            if self.srsCursor:
                self.srsCursor.close()
            if self.srsDB and self.srsDB.is_connected():
                self.srsDB.close()
        except Error as e:
            print(f"Error closing connection: {e}")

