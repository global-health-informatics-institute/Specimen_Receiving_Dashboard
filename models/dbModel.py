from models.dbConnection import cursor,conn

class Intermediate:

    def migrateAll(todaysDate):
        return ""
    
    def RemoveOutdated(todaysDate):
        return ""


class Summary:
    def __init__(self,tableName, columName, status):
        self.tableName = tableName
        self.columnName = columName
        self.status = status


    # ll be used to get the current value in the specified column name for the SummarySidebar 
    def getSummaryTotal(self):
        conn
        query = f"SELECT COUNT(*) FROM {self.tableName} WHERE {self.columnName} = ?"
        cursor.execute(query, (self.status,))
        result = cursor.fetchone()
        total = result[0] if result else 0
        conn.close()
        return total

    
    # ll run every 5 mins triggered by a cron job and update the fields the intermediate
    def updateSummaryFields(self):
        return ""
        # connect to mli

