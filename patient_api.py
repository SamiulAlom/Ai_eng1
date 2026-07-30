from flask import Flask, jsonify, request
from database import get_db_connection

app = Flask(__name__)


@app.route("/patients", methods=["GET"])
def get_patients():

    connection = None
    cursor = None

    try:
        connection = get_db_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM patients ORDER BY id")

        patients = cursor.fetchall()

        result = []

        for patient in patients:
            result.append({
                "id": patient[0],
                "name": patient[1],
                "age": patient[2],
                "cholesterol": patient[3]
            })

        return jsonify(result), 200

    except Exception as error:
        return jsonify({
            "message": "Something went wrong",
            "error": str(error)
        }), 500

    finally:
        if cursor:
            cursor.close()

        if connection:
            connection.close()

@app.route("/patients", methods=["POST"])
def add_patient():

    data = request.get_json()

    if not data:
        return jsonify({
            "message": "No data provided"
        }), 400

    if "name" not in data or "age" not in data or "cholesterol" not in data:
        return jsonify({
            "message": "Name, age and cholesterol are required"
        }), 400

    name = data["name"]
    age = data["age"]
    cholesterol = data["cholesterol"]

    if not isinstance(name, str):
        return jsonify({
            "message": "Name must be text"
        }), 400

    if not isinstance(age, int):
        return jsonify({
            "message": "Age must be an integer"
        }), 400

    if not isinstance(cholesterol, (int, float)):
        return jsonify({
            "message": "Cholesterol must be a number"
        }), 400

    if age <= 0:
        return jsonify({
            "message": "Age must be greater than 0"
        }), 400

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
        "id": new_id
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


@app.route("/patients/<int:id>", methods=["GET"])
def get_patient(id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE id = %s",
        (id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    connection.close()

    if patient is None:
        return jsonify({
            "message": "Patient not found"
        }), 404

    result = {
        "id": patient[0],
        "name": patient[1],
        "age": patient[2],
        "cholesterol": patient[3]
    }

    return jsonify(result), 200

if __name__ == "__main__":
    app.run(debug=True)