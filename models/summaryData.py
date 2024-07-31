from models.config import srsDB, Error, time_out, interval

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
        query = f"""
            SELECT
                COUNT(id) AS totalStatus
            FROM
                tests
            WHERE
                write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR;
        """
        return self._getSummaryCount(query)

    def getSummaryReceived(self):
        query = f"""
            SELECT
                COUNT(id) AS totalStatus
            FROM
                tests
            WHERE
                test_status IN ('0', '3', '4', '5')
                AND write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR 
        """
        return self._getSummaryCount(query)

    def getSummaryInprogress(self):
        query = f"""
            SELECT
                COUNT(id) AS totalStatus
            FROM
                tests
            WHERE
                test_status = 3
                AND write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR 
        """
        return self._getSummaryCount(query)

    def getSummaryPendingAuth(self):
        query = f"""
            SELECT
                COUNT(id) AS totalStatus
            FROM
                tests
            WHERE
                test_status = 4
                AND write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR 
        """
        return self._getSummaryCount(query)

    def getSummaryComplete(self):
        query = f"""
            SELECT
                COUNT(id) AS totalStatus
            FROM
                tests
            WHERE
                test_status IN ('5')
                AND write_date >= CURDATE() + INTERVAL {time_out} HOUR
                AND write_date <= CURDATE() + INTERVAL {interval} DAY + INTERVAL {time_out} HOUR 
        """        
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
