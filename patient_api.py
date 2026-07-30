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


@app.route("/patients", methods=["POST"])
def add_patient():

    data = request.get_json()

    name = data["name"]
    age = data["age"]
    cholesterol = data["cholesterol"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        INSERT INTO patients (name, age, cholesterol)
        VALUES (%s, %s, %s)
        RETURNING id
        """,
        (name, age, cholesterol)
    )

    new_id = cursor.fetchone()[0]

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Patient added successfully",
        "id": new_id,
        "name": name,
        "age": age,
        "cholesterol": cholesterol
    }), 201


@app.route("/patients/<int:id>", methods=["PUT"])
def update_patient(id):

    data = request.get_json()

    name = data["name"]
    age = data["age"]
    cholesterol = data["cholesterol"]

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        """
        UPDATE patients
        SET name = %s,
            age = %s,
            cholesterol = %s
        WHERE id = %s
        """,
        (name, age, cholesterol, id)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Patient updated successfully"
    }), 200



@app.route("/patients/<int:id>", methods=["DELETE"])
def delete_patient(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM patients WHERE id = %s",
        (id,)
    )

    connection.commit()

    cursor.close()
    connection.close()

    return jsonify({
        "message": "Patient deleted successfully"
    }), 200




if __name__ == "__main__":
    app.run(debug=True)