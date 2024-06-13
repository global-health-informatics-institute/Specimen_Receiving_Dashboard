import os
from flask import request, jsonify
import sqlite3
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR,'intermediateDB.db')

def receiveBarcode():
    data = request.json
    accession_id = data.get('ID')

    if not accession_id:
        return jsonify({"error": "No accession ID provided"}), 400

    # Update the test_status in the database
    try:
        conn = sqlite3.connect('models/intermediateDB.db')
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE tests
            SET test_status = 0
            WHERE accession_id = ?
        """, (accession_id,))
        conn.commit()

        if cursor.rowcount == 0:
            return jsonify({"error": "No matching accession ID found"}), 404
        
        return "ok", 200  # Return "ok" instead of JSON

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        conn.close()