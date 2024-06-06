import sqlite3

class MonthlyCounter:
    def __init__(self):
        self.connection = sqlite3.connect('models/intermediateDB.db')
        self.cursor = self.connection.cursor()

    def _get_summary_value(self, column_name):
        try:
            query = f'SELECT {column_name} FROM monthly_summary WHERE id = 1;'
            self.cursor.execute(query)
            result = self.cursor.fetchone()
            return result[0] if result and result[0] is not None else 0
        except Exception as e:
            print(f"An error occurred: {e}")
            return 0

    def getSummaryRegistered(self):
        return self._get_summary_value('monthly_registered')

    def getSummaryReceived(self):
        return self._get_summary_value('monthly_received')

    def getSummaryInprogress(self):
        return self._get_summary_value('monthly_progress')

    def getSummaryPendingAuth(self):
        return self._get_summary_value('monthly_pending')

    def getSummaryComplete(self):
        return self._get_summary_value('monthly_complete')

    def closeConn(self):
        self.cursor.close()
        self.connection.close()


class MonthlyIncrementor:
    def __init__(self):
        self.connection = sqlite3.connect('models/intermediateDB.db')
        self.cursor = self.connection.cursor()

    def _updateField(self, column_name):
        try:
            query = f'UPDATE monthly_summary SET {column_name} = {column_name} + 1 WHERE id = 1;'
            self.cursor.execute(query)
            self.connection.commit()  # Commit the transaction to save changes
        except Exception as e:
            print(f"An error occurred: {e}")

    def incrementRegistered(self):
        self._updateField('monthly_registered')

    def incrementReceived(self):
        self._updateField('monthly_received')

    def incrementInprogress(self):
        self._updateField('monthly_progress')

    def incrementPendingAuth(self):
        self._updateField('monthly_pending')

    def incrementComplete(self):
        self._updateField('monthly_complete')

    def closeConn(self):
        self.cursor.close()
        self.connection.close()

# incrementor = MonthlyIncrementor()
# incrementor.incrementRegistered()
# incrementor.incrementReceived()
# incrementor.incrementInprogress()
# incrementor.incrementPendingAuth()
# incrementor.incrementComplete()
# incrementor.closeConn()

