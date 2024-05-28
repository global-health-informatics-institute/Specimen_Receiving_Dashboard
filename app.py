from flask import Flask, render_template
from models.dbSetup import dbSetup
from models.summaryData import SummaryData

app = Flask(__name__)

@app.route("/dashboard/")
@app.route("/")
def index():
    return render_template("dashboard.base.html")

if __name__ == "__main__":
    dbSetup()


    # registered = Summary('tests', 'testType', 'registered')
    # totalRegistered = registered.getSummaryTotal()
    summaryDataObj = SummaryData()
    totalRegistered = summaryDataObj.getSummaryRegistered()
    summaryDataObj.closeConn()
    print(f"Total registered: {totalRegistered}")
    app.run(debug=True)
