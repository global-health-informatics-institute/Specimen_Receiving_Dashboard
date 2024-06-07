from flask import Flask, render_template, jsonify
from models.summaryData import SummaryData

app = Flask(__name__)

@app.route("/dashboard/")
@app.route("/")
def index():
    summary_data_obj = SummaryData()
    summary_content = {
        "summaryRegisteredTotal": summary_data_obj.getSummaryRegistered(),
        "summaryReceivedTotal": summary_data_obj.getSummaryReceived(),
        "summaryInProgressTotal": summary_data_obj.getSummaryInprogress(),
        "summaryPendingAuthTotal": summary_data_obj.getSummaryPendingAuth(),
        "summaryCompleteTotal": summary_data_obj.getSummaryComplete()
    }
    summary_data_obj.closeConn()

    return render_template(
        "dashboard1.template.html",
        **summary_content,
    )

@app.route("/summary_data")
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


    # summary_data_obj = SummaryData()
    # summary_content = {
    #     "summaryRegisteredTotal": summary_data_obj.getSummaryRegistered(),
    #     "summaryReceivedTotal": summary_data_obj.getSummaryReceived(),
    #     "summaryInProgressTotal": summary_data_obj.getSummaryInprogress(),
    #     "summaryPendingAuthTotal": summary_data_obj.getSummaryPendingAuth(),
    #     "summaryCompleteTotal": summary_data_obj.getSummaryComplete()
    # }
    # summary_data_obj.closeConn()

if __name__ == "__main__":
    app.run(debug=True)
