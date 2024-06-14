from config import srsDB, Error

class getTATData:
    def __init__(self):
        self.srsDB = srsDB()
        if self.srsDB is None:
            print("Failed to connect to srsDB.")
        else:
            self.srsCursor = self.srsDB.cursor()

    def _getSummaryValueHelper(self, test_short_name):
        try:
            if self.srsCursor:
                query = "SELECT targetTAT FROM test_definitions WHERE LOWER(test_short_name) = %s;"
                self.srsCursor.execute(query, (test_short_name.lower(),))
                result = self.srsCursor.fetchone()
                if result:
                    return result[0]  # Return the targetTAT as a string
                else:
                    print("No result found.")
                    return ""
            else:
                print("Cursor not initialized.")
                return ""
        except Error as e:
            print(f"Error: {e}")
            return ""

    def getTATForTestType(self, test_short_name):
        return self._getSummaryValueHelper(test_short_name)

    def closeConnections(self):
        try:
            if self.srsCursor:
                self.srsCursor.close()
            if self.srsDB and self.srsDB.is_connected():
                self.srsDB.close()
        except Error as e:
            print(f"Error closing connection: {e}")
# Example usage:
# tat_data = getTATData()
# target_tat = tat_data.getTATForTestType('APTT')
# print(target_tat)
# tat_data.closeConnections()

def getCurrent(self):
    ""

def getAverage(self):
    ""