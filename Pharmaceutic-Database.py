import sqlite3

# Connect to or create a SQLite database
conn = sqlite3.connect('Pharmaceutic-Database.db')
cur = conn.cursor()

# Load SQL script from file
with open("Pharmaceutic-Gestion.sql") as file:
    sql_script = file.read()

# Execute script to create database schema
cur.executescript(sql_script)

# 2. Prepare SQL INSERT queries for Patient, Doctor and Credentials tables
# Define sample data for patients, doctors, and credentials
patient_data = [
    (None, 1, '123456789', '1990-01-01', 'John', 'Doe', 1),
    (None, 2, '987654321', '1985-05-15', 'Jane', 'Smith', 1)
]

doctor_data = [
    (None, 3, 'INAMI123', 'Cardiology', 'Dr. Smith', 'Flyzer'),
    (None, 4, 'INAMI456', 'Pediatrics', 'Dr. Johnson', 'Johnson')
]

credentials_data = [
    (None, 'doctor@example.com', 'doctor123', 'Doctor'),
    (None, 'patient@example.com', 'patient123', 'Patient'),
    (None, 'admin@example.com', 'admin123', 'Admin')
]

# Insert data into Patient table
cur.executemany('''INSERT INTO Patient (idpatient, idperson, phonenumber, p_dateofbirth, p_name, p_lastname, is_active)
                   VALUES (?, ?, ?, ?, ?, ?, ?)''', patient_data)

# Insert data into Doctor table
cur.executemany('''INSERT INTO Doctor (iddoctor, idperson, inami, speciality, d_name, d_lastname)
                   VALUES (?, ?, ?, ?, ?, ?)''', doctor_data)

# Insert data into Credentials table
cur.executemany('''INSERT INTO Credentials (id, email, password, user_type)
                   VALUES (?, ?, ?, ?)''', credentials_data)

# 3. Relay information into Person table
# Inserting combined data from Patient and Doctor tables into Person table
cur.execute('''INSERT INTO Person (idperson, idpatient, iddoctor, firstname, familyname, dateofbirth)
               SELECT idperson, idpatient, NULL, p_name, p_lastname, p_dateofbirth FROM Patient
               UNION
               SELECT idperson, NULL, iddoctor, d_name, d_lastname, NULL FROM Doctor''')

#Execute script
cur.executescript(sql_script)

# Commit changes to the database
conn.commit()

# Close the connection
cur.close()
conn.close()