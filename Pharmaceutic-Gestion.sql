CREATE TABLE Person (
    idperson INTEGER PRIMARY KEY,
    firstname TEXT,
    familyname TEXT,
    dateofbirth DATE
);
 
CREATE TABLE Patient (
    idpatient INTEGER PRIMARY KEY,
    idperson INTEGER,
    phonenumber INTEGER,
    is_active BOOLEAN,
    FOREIGN KEY (idperson) REFERENCES Person(idperson)
);
 
CREATE TABLE Doctor (
    iddoctor INTEGER PRIMARY KEY,
    idperson INTEGER,
    inami INTEGER,
    speciality TEXT,
    FOREIGN KEY (idperson) REFERENCES Person(idperson)
);
 
CREATE TABLE Pharmacist (
    idpharmacist INTEGER PRIMARY KEY,
    idperson INTEGER,
    pharmacy_name TEXT,
    pharmacy_location TEXT,
    FOREIGN KEY (idperson) REFERENCES Person(idperson)
);

CREATE TABLE Medicine (
    id_medicine INTEGER PRIMARY KEY,
    name TEXT,
    content_quantity INTEGER,
    out_of_stock BOOLEAN,
    FOREIGN KEY (idpharmacist) REFERENCES Pharmacist(idpharmacist)
);

CREATE TABLE Appointment (
    id_appointment INTEGER PRIMARY KEY,
    idpatient INTEGER,
    iddoctor INTEGER,
    appointment_date DATE,
    appointment_time TIME,
    reason TEXT,
    prescription_status TEXT, -- Added field for prescription status
    FOREIGN KEY (idpatient) REFERENCES Patient(idpatient),
    FOREIGN KEY (iddoctor) REFERENCES Doctor(iddoctor)
);

CREATE TABLE Prescription (
    id_prescription INTEGER PRIMARY KEY,
    idpatient INTEGER,
    idpharmacist INTEGER,
    id_medicine INTEGER,
    quantity INTEGER,
    FOREIGN KEY (idpatient) REFERENCES Patient(idpatient),
    FOREIGN KEY (idpharmacist) REFERENCES Pharmacist(idpharmacist),
    FOREIGN KEY (id_medicine) REFERENCES Medicine(id_medicine)
);