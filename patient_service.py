from database import get_db_connection


def get_all_patients():

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM patients ORDER BY id"
    )

    patients = cursor.fetchall()

    cursor.close()
    connection.close()

    return patients


def get_patient_by_id(patient_id):

    connection = get_db_connection()
    cursor = connection.cursor()

    cursor.execute(
        "SELECT * FROM patients WHERE id = %s",
        (patient_id,)
    )

    patient = cursor.fetchone()

    cursor.close()
    connection.close()

    return patient


def create_patient(name, age, cholesterol):

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

    return new_id