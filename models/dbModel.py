# from models.dbConnection import cursor, conn

# departmentName = "Hematology"

# class Intermediate:

#     @staticmethod
#     def migrateAll(todaysDate):
#         return ""
    
#     @staticmethod
#     def RemoveOutdated(todaysDate):
#         return ""

# class Summary:
#     def __init__(self, columnName, status):
#         self.columnName = columnName
#         self.status = status

#     # ll be used to get the current value in the specified column name for the SummarySidebar 
#     def getSummaryTotal(self):
#         query = f"SELECT COUNT(*) FROM 'summary' WHERE {self.columnName} = ?"
#         cur = cursor()
#         cur.execute(query, (self.status,))
#         total = cur.fetchone()[0]
#         return total
    
#     # ll run every 5 mins triggered by a cron job and update the fields in the intermediate
#     def updateSummaryFields(self):
#         return ""
#         # connect to mli
# class test:
#     def __init__(self,testType):
#         self.testType = testType

#     def getTestTotal(self):
#         query = f"SELECT COUNT(*) FROM 'tests' WHERE testType = ?"
#         cur = cursor()
#         cur.execute(query, (self.testType))
#         total = cur.fetchone()[0]
#         return total