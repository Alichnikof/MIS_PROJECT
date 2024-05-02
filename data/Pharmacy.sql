CREATE TABLE Person (
    idperson INTEGER PRIMARY KEY AUTOINCREMENT,
    firstname TEXT,
    familyname TEXT,
    dateofbirth DATE
);
 
CREATE TABLE Patient (
    idpatient INTEGER PRIMARY KEY AUTOINCREMENT,
    idperson INTEGER,
    FOREIGN KEY (idperson) REFERENCES Person(idperson)
);
 
CREATE TABLE Doctor (
    iddoctor INTEGER PRIMARY KEY AUTOINCREMENT,
    idperson INTEGER,
    speciality TEXT,
    FOREIGN KEY (idperson) REFERENCES Person(idperson)
);
 
CREATE TABLE Pharmacist (
    idpharmacist INTEGER PRIMARY KEY AUTOINCREMENT,
    idperson INTEGER,
    FOREIGN KEY (idperson) REFERENCES Person(idperson)
);

CREATE TABLE Medicine (
    id_medicine INTEGER PRIMARY KEY AUTOINCREMENT,
    Med_name TEXT,
    content_quantity INTEGER,
    out_of_stock BOOLEAN
);

CREATE TABLE PatientMedication (
    idpatient INTEGER,
    id_medicine INTEGER,
    FOREIGN KEY (idpatient) REFERENCES Patient(idpatient),
    FOREIGN KEY (id_medicine) REFERENCES Medicine(id_medicine)
);

CREATE TABLE DoctorPatient (
    iddoctor INTEGER,
    idpatient INTEGER,
    PRIMARY KEY (iddoctor, idpatient),
    FOREIGN KEY (iddoctor) REFERENCES Doctor(iddoctor),
    FOREIGN KEY (idpatient) REFERENCES Patient(idpatient)
);

CREATE TABLE Prescription (
    id_prescription INTEGER PRIMARY KEY AUTOINCREMENT,
    idpatient INTEGER,
    id_medicine INTEGER,
    quantity INTEGER,
    FOREIGN KEY (idpatient) REFERENCES Patient(idpatient),
    FOREIGN KEY (id_medicine) REFERENCES Medicine(id_medicine),
    UNIQUE (idpatient, id_medicine) -- Ensures each patient can only have one prescription of each type of medication
);

CREATE TABLE Credentials (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    email VARCHAR UNIQUE,
    password VARCHAR,
    user_type VARCHAR,
    person_id INTEGER,
    FOREIGN KEY (person_id) REFERENCES Person(idperson) -- Linking person_id to idperson in Person table
);
