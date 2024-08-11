from models.config import srsDB, Error

class getTATData:
    def __init__(self, test_type):
        self.test_type = test_type
        self.srsDB = srsDB()
        if self.srsDB is None:
            print("Failed to connect to srsDB.")
        else:
            self.srsCursor = self.srsDB.cursor()

    def _getSummaryValueHelper(self):
        try:
            if self.srsCursor:
                query = "SELECT targetTAT FROM test_definitions WHERE LOWER(test_short_name) = %s;"
                self.srsCursor.execute(query, (self.test_type.lower(),))
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
            if self.srsCursor:
                self.srsCursor.close()
            if self.srsDB and self.srsDB.is_connected():
                self.srsDB.close()
            print(f"Error: {e}")


    def getTATForTestType(self):
        tat = self._getSummaryValueHelper()
        return tat
