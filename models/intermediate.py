# ToDo: implement the following: fetch data from IBlisDB within 3 days, move it to intermediate migrateAll()
# ToDo: update summaryData()
# ToDo: update tests()
# ToDo: update weekly_summary()
# ToDo: update monthly_summary()

import mysql.connector


# Configure MySQL connection
mydb = mysql.connector.connect(
    host="127.0.0.1",
    port = "3306",
    user="root",
    password="@clk11CK",
    database="test"
)

if mydb:
    print("connection ok")
else:
    print("connection Failed")


def migrateData():
    return ""
    # connect to iBlis database
    # fetch all data from virtual db test (virtual coss we joining couple of tables and selective columns)
    # filter in only entries within 3 days from date.now
    # return assosiative array from every record
    # update sqlite table "tests" in intermediate.db


    
# ll run every 5 mins triggered by a cron job and update the fields the intermediate
def updateSummaryFields(self):
    return ""
    # get number of rows wit status.register from table test and update to summary
    # get number of rows wit status.register from table test and update to summary
    # get number of rows wit status.register from table test and update to summary
    # get number of rows wit status.register from table test and update to summary
    # get number of rows wit status.register from table test and update to summary
