import os.path

from flask import Flask, request, render_template
from datetime import datetime
import sqlite3
import random
import json
from config.config_watcher import department_data

# define app
app = Flask(__name__)


@app.route("/", methods=["POST"])
# handle Post request
def GetBarcode():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    options = ["FBC", "ESR", "SC", "PBF"]
    type = random.choice(options)
    print(data)
    if len(data.get("ID")) == 10:
        cur.execute("INSERT INTO specimens (accession_number,status,type,department,time_received,time_registered)"
                    " VALUES (?,?,?,?,?,?)", (data.get("ID"), 'Received in Department', type,
                                              data.get("Department"), datetime.now(), datetime.now())
                    )
        conn.commit()
        conn.close()
    return "ok"


@app.route("/hema_dashboard")
def HeamatologyDashboard():
    conn = get_db_connection()
    # Summary Tab
    received = conn.execute(
        'SELECT status, count(*) FROM specimens where department ="hematology" and date(time_registered) = date("now") group by status').fetchall()
    counts = {}
    if received:
        for i in received:
            counts[i[0]] = i[1]
        registered = sum([i[1] for i in received])
    else:
        registered = 0
    # End of Summary Tab

    # FBC tab
    received_fbc = conn.execute(
        'SELECT status, count(*) FROM specimens where department ="hematology" and type = "FBC" and date(time_registered) = date("now") group by status').fetchall()
    counts_fbc = {}
    if received_fbc:
        for i in received_fbc:
            counts_fbc[i[0]] = i[1]
    # End of FBC tab

    # ESR Tab
    received_esr = conn.execute(
        'SELECT status, count(*) FROM specimens where department ="hematology" and type = "ESR" and date(time_registered) = date("now") group by status').fetchall()
    counts_esr = {}
    if received_esr:
        for i in received_esr:
            counts_esr[i[0]] = i[1]
    # End of ESR tab

    # Sickle Cell Tab
    received_sc = conn.execute(
        'SELECT status, count(*) FROM specimens where department ="hematology" and type = "SC" and date(time_registered) = date("now") group by status').fetchall()
    counts_sc = {}
    if received_sc:
        for i in received_sc:
            counts_sc[i[0]] = i[1]
    # End of Sickle Cell tab

    # PBF Tab
    received_pbf = conn.execute(
        'SELECT status, count(*) FROM specimens where department ="hematology" and type = "PBF" and date(time_registered) = date("now") group by status').fetchall()
    counts_pbf = {}
    if received_pbf:
        for i in received_pbf:
            counts_pbf[i[0]] = i[1]
    # End of PBF tab

    conn.close()
    return render_template("HeamatologyDashboard.html", test_counts=counts, registered=registered,
                           counts_fbc=counts_fbc, counts_esr=counts_esr, counts_sc=counts_sc, counts_pbf=counts_pbf,
                           department_data=department_data)


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
    specimens = conn.execute('SELECT * FROM specimens where department ="hematology" and'
                             ' status not in ("Analysis Complete","Rejected") ').fetchall()
    return render_template("specimens.html", specimens=specimens)


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0")
