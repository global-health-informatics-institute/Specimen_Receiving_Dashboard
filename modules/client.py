from flask import request, jsonify
import mysql.connector
from mysql.connector import Error

def receiveBarcode():
    data = request.json
    accession_id = data.get('ID')

    if not accession_id:
        return jsonify({"error": "No accession ID provided"}), 400

    # Update the test_status in the database
    try:
        connection = mysql.connector.connect(
            host="192.168.1.164",
            port="3306",
            user="ghii",
            password="..blackEvil89",
            database="Haematology",
            auth_plugin='mysql_native_password',
        )

        if connection.is_connected():
            cursor = connection.cursor()

            cursor.execute("""
                UPDATE tests
                SET test_status = 0
                WHERE accession_id = %s
                AND test_status NOT IN ( '0', '3', '4', '5','9')
            """, (accession_id,))

            connection.commit()

            if cursor.rowcount == 0:
                return jsonify({"error": "No matching accession ID found"}), 404
            else:
                cursor.execute("UPDATE weekly_summary SET weekly_received = weekly_received + 1 WHERE id = 1;")
                cursor.execute("UPDATE monthly_summary SET monthly_received = monthly_received + 1 WHERE id = 1;")
                connection.commit()

            return "ok", 200  # Return "ok" instead of JSON

    except Error as e:
        return jsonify({"error": str(e)}), 500

    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()
