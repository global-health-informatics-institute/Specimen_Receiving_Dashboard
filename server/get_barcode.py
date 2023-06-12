import os.path

from flask import Flask, request, render_template
from datetime import datetime
import sqlite3
import json
# define app
app = Flask(__name__)


@app.route("/", methods=["POST"])
# handle Post request
def GetBarcode():
   data = request.json
   conn = get_db_connection()
   cur = conn.cursor()

   cur.execute("INSERT INTO specimens (accession_number,status, department,time_received,time_registered)"
               " VALUES (?, ?,?, ?, ?)", (data.get("accession_id"), 'Received in Department',
                                         data.get("department"), datetime.now(), datetime.now())
               )
   conn.commit()
   conn.close()
   return "ok"


@app.route("/hema_dashboard")
def HeamatologyDashboard():
    conn = get_db_connection()
    received = conn.execute('SELECT status, count(*) FROM specimens where department ="Haematology" group by status').fetchall()
    counts = {}
    for i in received:
        counts[i[0]] = i[1]
    print(received[0])
    conn.close()
    return render_template("HeamatologyDashboard.html", test_counts=counts)


def get_db_connection():
    db_initialized = os.path.isfile('database.db')
    connection = sqlite3.connect("database.db")
    if not db_initialized:
        with open('schema.sql') as f:
            connection.executescript(f.read())

    connection.row_factory = sqlite3.Row
    return connection


@app.route("/simulate_progress", methods=["POST", "GET"])
def simulate_progress():
    conn = get_db_connection()
    status = ["Registered", "Received in Department", "In Progress", "Pending Authorization", "Analysis Complete"]
    if request.method == "POST":
        id = request.json["ID"]
        specimen = conn.execute('SELECT * FROM specimens where specimen_id = ?', (id,)).fetchone()
        next_state = status[status.index(specimen["status"]) + 1]
        conn.execute('UPDATE specimens SET status= ? where specimen_id = ?', (next_state, id,))
        conn.commit()
    specimens = conn.execute('SELECT * FROM specimens where department ="Haematology" and'
                                 ' status not in ("Analysis Complete","Rejected") ').fetchall()
    return render_template("specimens.html", specimens=specimens)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
