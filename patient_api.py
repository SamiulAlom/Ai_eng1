from flask import Flask, jsonify, request
from database import get_db_connection

app = Flask(__name__)


@app.route("/patients", methods=["GET"])
def get_patients():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute("SELECT * FROM patients ORDER BY id")

    patients = cursor.fetchall()

    cursor.close()
    connection.close()

    result = []

    for patient in patients:
        result.append({
            "id": patient[0],
            "name": patient[1],
            "age": patient[2],
            "cholesterol": patient[3]
        })

    return jsonify(result), 200


if __name__ == "__main__":
    app.run(debug=True)