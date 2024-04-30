import sqlite3

# Connect to or create a SQLite database
conn = sqlite3.connect('PharmacyGestion400.db')
cur = conn.cursor()

# Create tables
cur.execute('''CREATE TABLE IF NOT EXISTS Person (
                    idperson INTEGER PRIMARY KEY,
                    firstname TEXT,
                    familyname TEXT,
                    dateofbirth DATE
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Patient (
                    idpatient INTEGER PRIMARY KEY,
                    idperson INTEGER,
                    FOREIGN KEY (idperson) REFERENCES Person(idperson)
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Doctor (
                    iddoctor INTEGER PRIMARY KEY,
                    idperson INTEGER,
                    speciality TEXT,
                    FOREIGN KEY (idperson) REFERENCES Person(idperson)
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Pharmacist (
                    idpharmacist INTEGER PRIMARY KEY,
                    idperson INTEGER,
                    pharmacy_name TEXT,
                    pharmacy_location TEXT,
                    FOREIGN KEY (idperson) REFERENCES Person(idperson)
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Medicine (
                    id_medicine INTEGER PRIMARY KEY,
                    Med_name TEXT,
                    content_quantity INTEGER,
                    out_of_stock BOOLEAN,
                    idpharmacist INTEGER,
                    FOREIGN KEY (idpharmacist) REFERENCES Pharmacist(idpharmacist)
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Prescription (
                    id_prescription INTEGER PRIMARY KEY,
                    idpatient INTEGER,
                    idpharmacist INTEGER,
                    id_medicine INTEGER,
                    quantity INTEGER,
                    FOREIGN KEY (idpatient) REFERENCES Patient(idpatient),
                    FOREIGN KEY (idpharmacist) REFERENCES Pharmacist(idpharmacist),
                    FOREIGN KEY (id_medicine) REFERENCES Medicine(id_medicine)
                )''')

cur.execute('''CREATE TABLE IF NOT EXISTS Credentials (
                    id INTEGER PRIMARY KEY,
                    email TEXT UNIQUE,
                    password TEXT,
                    user_type TEXT
                )''')

# Insert sample data
person_data = [('John', 'Doe', '1990-01-01'), ('Jane', 'Smith', '1985-05-15'), ('Dr. Smith', '', ''), ('Dr. Johnson', '', ''), ('Pharmacist Name', '', '')]

cur.executemany('''INSERT INTO Person (firstname, familyname, dateofbirth)
                   VALUES (?, ?, ?)''', person_data)

patient_data = [(1,), (2,)]

cur.executemany('''INSERT INTO Patient (idperson)
                   VALUES (?)''', patient_data)

doctor_data = [(3, 'Cardiology'), (4, 'Pediatrics')]

cur.executemany('''INSERT INTO Doctor (idperson, speciality)
                   VALUES (?, ?)''', doctor_data)

pharmacist_data = [(5, 'Pharmacy A', 'Location A')]

cur.executemany('''INSERT INTO Pharmacist (idperson, pharmacy_name, pharmacy_location)
                   VALUES (?, ?, ?)''', pharmacist_data)

medicine_data = [('Paracetamol', 20, 0, 1), ('Amoxicillin', 15, 0, 1)]

cur.executemany('''INSERT INTO Medicine (Med_name, content_quantity, out_of_stock, idpharmacist)
                   VALUES (?, ?, ?, ?)''', medicine_data)

prescription_data = [(1, 1, 1, 2), (2, 2, 1, 1)]

cur.executemany('''INSERT INTO Prescription (idpatient, idpharmacist, id_medicine, quantity)
                   VALUES (?, ?, ?, ?)''', prescription_data)

credentials_data = [('pharmacist@example.com', 'pharmacist123', 'Pharmacist'), ('doctor@example.com', 'doctor123', 'Doctor'), ('patient@example.com', 'patient123', 'Patient')]

cur.executemany('''INSERT INTO Credentials (email, password, user_type)
                   VALUES (?, ?, ?)''', credentials_data)

# Commit changes to the database
conn.commit()

# Close the connection
cur.close()
conn.close()