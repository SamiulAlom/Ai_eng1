# import psycopg2
#
#
# connection = psycopg2.connect(
#     host="localhost",
#     database="ai_engineering",
#     user="postgres",
#     password="",
#     port="5432"
# )
#
# print("Database connected successfully!")
#
# connection.close()


import psycopg2


connection = psycopg2.connect(
    host="localhost",
    database="ai_engineering",
    user="postgres",
    password="",
    port="5432"
)

cursor = connection.cursor()

cursor.execute("SELECT * FROM patients")

patients = cursor.fetchall()

for patient in patients:
    print(patient)

# cursor.execute(
#     """
#     INSERT INTO patients (name, age, cholesterol)
#     VALUES (%s, %s, %s)
#     """,
#     ("Rahim", 60, 320)
# )
#
# connection.commit()
#
# print("Patient inserted successfully!")

# patients = cursor.fetchall()
# for patient in patients:
#     print(patient)

cursor.close()
connection.close()