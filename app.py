from flask import Flask, render_template
from models.dbSetup import dbSetup
from models.dbModel import Summary

app = Flask(__name__)

@app.route("/dashboard/")
@app.route("/")
def index():
    return render_template("dashboard.base.html")

if __name__ == "__main__":
    dbSetup()
    registered = Summary('tests', 'testType', 'registered')
    totalRestered = registered.getSummaryTotal()
    print(f"Total is: {totalRestered}")
    app.run(debug=True)
