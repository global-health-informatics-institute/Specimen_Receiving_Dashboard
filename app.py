from flask import Flask, jsonify, render_template
from models.config import department, testType1, testType2, testType3, testType4
from models.dbSetup import createView, dbSetup, dropView
from models.intermediate import migrateAllUnique, updateExisting
from models.monthlyData import MonthlyCounter
from models.summaryData import SummaryData
from models.tests import TestsData
from models.tat import TATData
from models.weeklyData import WeeklyCounter
from modules.client import receiveBarcode
from scripts.erasers import clearTable

app = Flask(__name__)

def get_test_content(test_type, prefix):
    test_data_obj = TestsData(test_type)
    test_content = {
        f"registered{prefix}": test_data_obj.getRegistered(),
        f"received{prefix}": test_data_obj.getReceived(),
        f"inProgress{prefix}": test_data_obj.getInProgress(),
        f"pendingAuth{prefix}": test_data_obj.getPendingAuth(),
        f"complete{prefix}": test_data_obj.getComplete()
    }
    test_data_obj.closeConn()
    return test_content


@app.route("/", methods=["POST"])
def client():
    return receiveBarcode()

# drop view at 07:00
# create view at 07:02
# migrateData every morning 07:05
# weeklyEraser first day of the week
# monthlyEraser first day of the month
# update periodically

# drop view at 07:00
@app.route("/dropView/..blackEvil")
def runDropView():
    return dropView()
# red
@app.route("/dbSetup/..blackEvil")
def runDBSetup():
    if dbSetup():
        return dbSetup()
    else:
        return "dbSetUp is Up and running"
    


# create view at 07:02
@app.route("/createView/")
def runCreateView():
    return createView()

# migrateData every morning 07:05
@app.route("/migrateData/")
def runMigrateData():
    if migrateAllUnique():
        return migrateAllUnique()
    else:
        return "This returned none"

# weeklyEraser first day of the week
@app.route("/weeklyEraser/")
def runWeeklyEraser():
    if clearTable("weekly_summary"):
        return clearTable("weekly_summary")
    else:
        return "This returned a none"

# monthlyEraser first day of the month
@app.route("/monthlyEraser/")
def runMonthlyEraser():
    if clearTable("monthly_summary"):
        return clearTable("monthly_summary")
    else:
        return "This returned a none"

# update periodically
@app.route("/updatePeriodically/")
def runUpdatePeriodically():
    return updateExisting()

@app.route("/dashboard/")
def index():
    content = {
        "departmentName": department,
        "testType1": testType1,
        "testType2": testType2,
        "testType3": testType3,
        "testType4": testType4,
    }
    
    summary_data_obj = SummaryData()
    summary_content = {
        "summaryRegisteredTotal": summary_data_obj.getSummaryRegistered(),
        "summaryReceivedTotal": summary_data_obj.getSummaryReceived(),
        "summaryInProgressTotal": summary_data_obj.getSummaryInprogress(),
        "summaryPendingAuthTotal": summary_data_obj.getSummaryPendingAuth(),
        "summaryCompleteTotal": summary_data_obj.getSummaryComplete()
    }
    summary_data_obj.closeConn()

    test_content1 = get_test_content(testType1, '1')
    test_content2 = get_test_content(testType2, '2')
    test_content3 = get_test_content(testType3, '3')
    test_content4 = get_test_content(testType4, '4')

    tat_content = {
        "target1": TATData(testType1).targetTAT(),
        "target2": TATData(testType2).targetTAT(),
        "target3": TATData(testType3).targetTAT(),
        "target4": TATData(testType4).targetTAT()
    }

    counter = WeeklyCounter()
    weekly_content = {
        "weeklyRegistered": counter.getSummaryRegistered(),
        "weeklyRecieved": counter.getSummaryReceived(),
        "weeklyProgress": counter.getSummaryInprogress(),
        "weeklyPending": counter.getSummaryPendingAuth(),
        "weeklyComplete": counter.getSummaryComplete()
    }
    counter.closeConn()

    counter_monthly = MonthlyCounter()
    monthly_content = {
        "monthlyRegistered": counter_monthly.getSummaryRegistered(),
        "monthlyRecieved": counter_monthly.getSummaryReceived(),
        "monthlyProgress": counter_monthly.getSummaryInprogress(),
        "monthlyPending": counter_monthly.getSummaryPendingAuth(),
        "monthlyComplete": counter_monthly.getSummaryComplete()
    }
    counter_monthly.closeConn()

    return render_template(
        "dashboard.template.html",
        **content,
        **summary_content,
        **test_content1,
        **test_content2,
        **test_content3,
        **test_content4,
        **tat_content,
        **weekly_content,
        **monthly_content
    )

@app.route("/summary_content")
def summary_data():
    summary_data_obj = SummaryData()
    summary_content = {
        "summaryRegisteredTotal": summary_data_obj.getSummaryRegistered(),
        "summaryReceivedTotal": summary_data_obj.getSummaryReceived(),
        "summaryInProgressTotal": summary_data_obj.getSummaryInprogress(),
        "summaryPendingAuthTotal": summary_data_obj.getSummaryPendingAuth(),
        "summaryCompleteTotal": summary_data_obj.getSummaryComplete()
    }
    summary_data_obj.closeConn()
    return jsonify(summary_content)

@app.route("/test_content1")
def test_content1():
    test_content1 = get_test_content(testType1, '1')
    return jsonify(test_content1)

@app.route("/test_content2")
def test_content2():
    test_content2 = get_test_content(testType2, '2')
    return jsonify(test_content2)

@app.route("/test_content3")
def test_content3():
    test_content3 = get_test_content(testType3, '3')
    return jsonify(test_content3)

@app.route("/test_content4")
def test_content4():
    test_content4 = get_test_content(testType4, '4')
    return jsonify(test_content4)

@app.route("/tat_content")
def tat_content():
    tat_content = {
        "target1": TATData(testType1).targetTAT(),
        "target2": TATData(testType2).targetTAT(),
        "target3": TATData(testType3).targetTAT(),
        "target4": TATData(testType4).targetTAT()
    }
    return jsonify(tat_content)

@app.route("/weekly_content")
def weekly_content():
    counter = WeeklyCounter()
    weekly_content = {
        "weeklyRegistered": counter.getSummaryRegistered(),
        "weeklyRecieved": counter.getSummaryReceived(),
        "weeklyProgress": counter.getSummaryInprogress(),
        "weeklyPending": counter.getSummaryPendingAuth(),
        "weeklyComplete": counter.getSummaryComplete()
    }
    counter.closeConn()
    return jsonify(weekly_content)

@app.route("/monthly_content")
def monthly_content():
    counter_monthly = MonthlyCounter()
    monthly_content = {
        "monthlyRegistered": counter_monthly.getSummaryRegistered(),
        "monthlyRecieved": counter_monthly.getSummaryReceived(),
        "monthlyProgress": counter_monthly.getSummaryInprogress(),
        "monthlyPending": counter_monthly.getSummaryPendingAuth(),
        "monthlyComplete": counter_monthly.getSummaryComplete()
    }
    counter_monthly.closeConn()
    return jsonify(monthly_content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
