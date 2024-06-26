# Pharmacy Management System - Pharmacy Database Page
import sqlite3 as sq
import os

# Path correction using raw string or replace with forward slashes
database_path = 'pharmacydatabase.db'
# or "Lab 3/healthdatabase (1).sql"
sql_script_path = r"MIS_PROJECT\data\Pharmacy.sql"

# Check if the database file exists
if not os.path.exists(database_path):
    # Connect to or create a SQLite database
    conn = sq.connect(database_path)
    cursor = conn.cursor()
    # Load SQL script from file
    with open(sql_script_path) as file:
        sql_script = file.read()
    # Execute script
    cursor.executescript(sql_script)
    # Commit the changes and close within the if block
    conn.commit()
    cursor.close()
    conn.close()

# Reconnect to ensure the connection is always defined
conn = sq.connect(database_path)
cursor = conn.cursor()

# Insert example data
# Inserting example persons into the database
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('John', 'Doe', '1980-01-15')")
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('Jane', 'Smith', '1975-05-20')")
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('Alice', 'Johnson', '1990-08-10')")
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('Bob', 'Williams', '1988-03-25')")
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('Emma', 'Brown', '1992-11-05')")
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('Michael', 'Clark', '1985-09-12')")
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('Sophia', 'Martinez', '1983-07-30')")
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('Daniel', 'Garcia', '1995-04-18')")
cursor.execute(
    "INSERT INTO Person (firstname, familyname, dateofbirth) VALUES ('Pharma', 'Boss', '1998-08-18')")

# Inserting example doctors into the database
cursor.execute(
    "INSERT INTO Doctor (idperson) VALUES (1)")
cursor.execute(
    "INSERT INTO Doctor (idperson) VALUES (2)")

# Inserting example patients into the database
for i in range(3, 9):
    cursor.execute(f"INSERT INTO Patient (idperson) VALUES ({i})")

# Assigning patients to doctors into the database
cursor.execute("INSERT INTO DoctorPatient (iddoctor, idpatient) VALUES (1, 1)")
cursor.execute("INSERT INTO DoctorPatient (iddoctor, idpatient) VALUES (1, 2)")
cursor.execute("INSERT INTO DoctorPatient (iddoctor, idpatient) VALUES (1, 3)")
cursor.execute("INSERT INTO DoctorPatient (iddoctor, idpatient) VALUES (2, 4)")
cursor.execute("INSERT INTO DoctorPatient (iddoctor, idpatient) VALUES (2, 5)")
cursor.execute("INSERT INTO DoctorPatient (iddoctor, idpatient) VALUES (2, 6)")

# Inserting example medicines into the database
cursor.execute(
    "INSERT INTO Medicine (Med_name, content_quantity) VALUES ('Paracetamol', 5)")
cursor.execute(
    "INSERT INTO Medicine (Med_name, content_quantity) VALUES ('Amoxicillin', 10)")
cursor.execute(
    "INSERT INTO Medicine (Med_name, content_quantity) VALUES ('Aspirin', 1)")

# Making prescriptions from doctors to patients into the database
cursor.execute(
    "INSERT INTO Prescription (idpatient, id_medicine, quantity) VALUES (1, 1, 2)")
cursor.execute(
    "INSERT INTO Prescription (idpatient, id_medicine, quantity) VALUES (2, 2, 1)")
cursor.execute(
    "INSERT INTO Prescription (idpatient, id_medicine, quantity) VALUES (3, 3, 3)")
cursor.execute(
    "INSERT INTO Prescription (idpatient, id_medicine, quantity) VALUES (1, 3, 1)")
cursor.execute(
    "INSERT INTO Prescription (idpatient, id_medicine, quantity) VALUES (1, 2, 2)")
cursor.execute(
    "INSERT INTO Prescription (idpatient, id_medicine, quantity) VALUES (4, 3, 1)")

# Inserting example pharmacist into the database
cursor.execute("INSERT INTO Pharmacist (idperson) VALUES (9)")

# Insert example credentials for patients into the database
patients_credentials = [
    ('patient1@example.com', 'password', 'patient', 3),
    ('patient2@example.com', 'password', 'patient', 4),
    ('patient3@example.com', 'password', 'patient', 5),
    ('patient4@example.com', 'password', 'patient', 6),
    ('patient5@example.com', 'password', 'patient', 7),
    ('patient6@example.com', 'password', 'patient', 8),
]
# Insert credentials for patients into the database
cursor.executemany(
    "INSERT INTO Credentials (email, password, user_type, person_id) VALUES (?, ?, ?, ?)", patients_credentials)

# Insert example credentials for doctors into the database
doctors_credentials = [
    # Assuming the ID of the first doctor is 1
    ('doctor1@example.com', 'password', 'doctor', 1),
    # Assuming the ID of the second doctor is 2
    ('doctor2@example.com', 'password', 'doctor', 2),
]
cursor.executemany(
    "INSERT INTO Credentials (email, password, user_type, person_id) VALUES (?, ?, ?, ?)", doctors_credentials)

# Insert example credentials for pharmacists into the database
pharmacists_credentials = [
    ('pharmacist1@example.com', 'password', 'pharmacist', 9)]
cursor.executemany(
    "INSERT INTO Credentials (email, password, user_type, person_id) VALUES (?, ?, ?,?)", pharmacists_credentials)

# Commit the changes
conn.commit()
# Close the connection when done
cursor.close()
conn.close()
