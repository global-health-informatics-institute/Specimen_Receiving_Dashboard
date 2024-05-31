from flask import Flask, render_template
from models.dbSetup import dbSetup, department, testType1, testType2, testType3, testType4
from models.summaryData import SummaryData
from models.tests import TestsData
from models.tat import TATData

app = Flask(__name__)

@app.route("/dashboard/")
def index():
    
    content = {
        "departmentName": department,
        "testType1": testType1,
        "testType2": testType2,
        "testType3": testType3,
        "testType4": testType4,
    }
    summaryDataObj = SummaryData()
    summaryContent = {
        "summaryRegisteredTotal": summaryDataObj.getSummaryRegistered(),
        "summaryReceivedTotal": summaryDataObj.getSummaryReceived(),
        "summaryInProgressTotal": summaryDataObj.getSummaryInprogress(),
        "summaryPendingAuthTotal": summaryDataObj.getSummaryPendingAuth(),
        "summaryCompleteTotal": summaryDataObj.getSummaryComplete()
    }
    summaryDataObj.closeConn()
    # -----------------------
    testDataObj1 = TestsData(testType1)
    testContent1 = {
        "registered1": testDataObj1.getRegistered(),
        "received1": testDataObj1.getReceived(),
        "inProgress1": testDataObj1.getInProgress(),
        "pendingAuth1": testDataObj1.getPendingAuth(),
        "complete1": testDataObj1.getComplete()
    }
    testDataObj1.closeConn()
    # -----------------------
    testDataObj2 = TestsData(testType2)
    testContent2 = {
        "registered2": testDataObj2.getRegistered(),
        "received2": testDataObj2.getReceived(),
        "inProgress2": testDataObj2.getInProgress(),
        "pendingAuth2": testDataObj2.getPendingAuth(),
        "complete2": testDataObj2.getComplete()
    }
    testDataObj2.closeConn()
    # -----------------------
    testDataObj3 = TestsData(testType3)
    testContent3 = {
        "registered3": testDataObj3.getRegistered(),
        "received3": testDataObj3.getReceived(),
        "inProgress3": testDataObj3.getInProgress(),
        "pendingAuth3": testDataObj3.getPendingAuth(),
        "complete3": testDataObj3.getComplete()
    }
    testDataObj3.closeConn()

    # -----------------------
    testDataObj4 = TestsData(testType4)
    testContent4 = {
        "registered4": testDataObj4.getRegistered(),
        "received4": testDataObj4.getReceived(),
        "inProgress4": testDataObj4.getInProgress(),
        "pendingAuth4": testDataObj4.getPendingAuth(),
        "complete4": testDataObj4.getComplete()
    }
    testDataObj4.closeConn()

    # -------------------------------
    tatContent = {
        "tat1": TATData(testType1).targetTAT(),
        "tat2": TATData(testType2).targetTAT(),
        "tat3": TATData(testType3).targetTAT(),
        "tat4": TATData(testType4).targetTAT()
    }



    return render_template("dashboard.template.html", **content, **summaryContent, **testContent1, **testContent2, **testContent3, **testContent4, **tatContent)

if __name__ == "__main__":
    app.run(debug=True)

