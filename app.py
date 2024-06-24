from flask import Flask, jsonify, render_template
from models.config import department, testType1, testType2, testType3, testType4
from models.monthlyData import MonthlyCounter
# from models.populateSetUp import populateDepartmentDefinitions, populateMonthlySummary, populateStatusDefinitions, populateTestDefinitions, populateWeeklySummary
# from models.setUp import createIntermediate, defineTables
from models.summaryData import SummaryData
from models.tatCurrentPlusAverage import tatAverage, tatCurrent
from models.tests import TestsData
from models.tat import getTATData as TATData
from models.updateEntries import updateEntries
from models.weeklyData import WeeklyCounter
from modules.client import receiveBarcode

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

@app.route("/update/")
def update():
    return updateEntries()

# @app.route("/setUp/")
# def setUp():
#     createIntermediate()
#     defineTables()
#     populateDepartmentDefinitions()
#     populateTestDefinitions()
#     populateStatusDefinitions()
#     populateWeeklySummary()
#     populateMonthlySummary()
#     return "ok"



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
    summary_data_obj.closeConnections()

    test_content1 = get_test_content(testType1, '1')
    test_content2 = get_test_content(testType2, '2')
    test_content3 = get_test_content(testType3, '3')
    test_content4 = get_test_content(testType4, '4')

    tat_content = {
        "target1": TATData(testType1).getTATForTestType(),
        "target2": TATData(testType2).getTATForTestType(),
        "target3": TATData(testType3).getTATForTestType(),
        "target4": TATData(testType4).getTATForTestType()
    }

    tat_current = {
        "current1": tatCurrent(testType1),
        "current2": tatCurrent(testType2),
        "current3": tatCurrent(testType3),
        "current4": tatCurrent(testType4)
    }

    tat_average = {
        "average1": tatAverage(testType1),
        "average2": tatAverage(testType2),
        "average3": tatAverage(testType3),
        "average4": tatAverage(testType4)
    }

    counter = WeeklyCounter()
    weekly_content = {
        "weeklyRegistered": counter.getSummaryRegistered(),
        "weeklyRecieved": counter.getSummaryReceived(),
        "weeklyProgress": counter.getSummaryInprogress(),
        "weeklyPending": counter.getSummaryPendingAuth(),
        "weeklyComplete": counter.getSummaryComplete()
    }
    counter.closeConnections()

    counter_monthly = MonthlyCounter()
    monthly_content = {
        "monthlyRegistered": counter_monthly.getSummaryRegistered(),
        "monthlyRecieved": counter_monthly.getSummaryReceived(),
        "monthlyProgress": counter_monthly.getSummaryInprogress(),
        "monthlyPending": counter_monthly.getSummaryPendingAuth(),
        "monthlyComplete": counter_monthly.getSummaryComplete()
    }
    counter_monthly.closeConnections()

    return render_template(
        "dashboard.template.html",
        **content,
        **summary_content,
        **test_content1,
        **test_content2,
        **test_content3,
        **test_content4,
        **tat_content,
        **tat_current,
        **tat_average,
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
    summary_data_obj.closeConnections()
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
        "target1": TATData(testType1).getTATForTestType(),
        "target2": TATData(testType2).getTATForTestType(),
        "target3": TATData(testType3).getTATForTestType(),
        "target4": TATData(testType4).getTATForTestType()
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
    counter.closeConnections()
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
    counter_monthly.closeConnections()
    return jsonify(monthly_content)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
