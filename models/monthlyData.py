import sqlite3
conn = sqlite3.connect('models/intermediateDB.db')


class Database:
    def __init__(self):
        self.connection = conn
        self.cursor = self.connection.cursor()

    def getSummaryRegistered(self):
        query = 'SELECT COUNT(id) AS totalStatus FROM monthly_summary WHERE lcase(test_status) = "registered";'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status
    

    def getSummaryReceived(self):
        query = 'SELECT COUNT(id) AS totalStatus FROM monthly_summary WHERE lcase(test_status) = "received";'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status
    

    def getSummaryInprogress(self):
        query = 'SELECT COUNT(id) AS totalStatus FROM monthly_summary WHERE lcase(test_status) = "in_progress";'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status
    

    def getSummaryPendingAuth(self):
        query = 'SELECT COUNT(id) AS totalStatus FROM monthly_summary WHERE lcase(test_status) = "pending_auth";'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status
    

    def getSummaryComplete(self):
        query = 'SELECT COUNT(id) AS totalStatus FROM monthly_summary WHERE lcase(test_status) = "complete";'
        self.cursor.execute(query)
        result = self.cursor.fetchone()
        total_status = result[0] if result else 0
        return total_status
    
    
    
    
    def closeConn(self):
        self.cursor.close()