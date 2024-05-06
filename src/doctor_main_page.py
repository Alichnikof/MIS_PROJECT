import tkinter as tk
from main_page import MainPage, messagebox, sqlite3
from tkinter import Button, Label, Frame, Scrollbar, Listbox, END, messagebox, ttk


class DoctorMainPage(MainPage):
    def __init__(self, doctor_id):
        super().__init__("doctor")
        self.doctor_id = doctor_id
        self.selected_patient = None
        self.selected_medication = None
        self.patients = None  # Initialize patients attribute
        self.populate_patients_list()

        self.prescribe_button = Button(
            self.root, text="Prescribe Medication", command=self.prescribe_medication)
        self.prescribe_button.pack(pady=5)

        self.register_patient_button = Button(
            self.root, text="Register Patient", command=self.open_registration_window)
        self.register_patient_button.pack(pady=5)

        self.medication_listbox.bind(
            "<<ListboxSelect>>", self.on_medication_select)

    def populate_patients_list(self):
        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Person.firstname, Patient.idpatient
                FROM Patient
                INNER JOIN DoctorPatient ON Patient.idpatient = DoctorPatient.idpatient
                INNER JOIN Person ON Patient.idperson = Person.idperson
                WHERE DoctorPatient.iddoctor = ?""", (self.doctor_id,))
            self.patients = cursor.fetchall()  # Store patients in attribute

            self.patients_frame = Frame(self.root)
            self.patients_frame.pack(pady=10)
            self.patients_label = Label(
                self.patients_frame, text="Patients List:")
            self.patients_label.pack(side="left")

            # Create a dropdown menu for patients
            self.patients_combobox = ttk.Combobox(
                self.patients_frame, width=40, state="readonly")
            self.patients_combobox['values'] = [patient[0]
                                                for patient in self.patients]
            self.patients_combobox.pack(side="left", fill="both", expand=True)

            self.patients_combobox.bind(
                "<<ComboboxSelected>>", self.on_patient_select)

        except sqlite3.Error as e:
            print("Database error:", e)

        finally:
            conn.close()

    def prescribe_medication(self):
        if not self.selected_patient:
            messagebox.showerror("Error", "Please select a patient.")
            return
        if not self.selected_medication:
            messagebox.showerror(
                "Error", "Please select a medication to prescribe.")
            return

        # Corrected to retrieve idpatient
        patient_id = self.selected_patient[1]
        medication_id = self.selected_medication[1]

        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Prescription WHERE idpatient=? AND id_medicine=?", (patient_id, medication_id))
            existing_prescription = cursor.fetchone()

            # Check if the prescription exists and is retrieved correctly
            if existing_prescription:
                cursor.execute(
                    "UPDATE Prescription SET quantity = quantity + 1 WHERE id_prescription=?", (existing_prescription[0],))
            else:
                cursor.execute(
                    "INSERT INTO Prescription (idpatient, id_medicine, quantity) VALUES (?, ?, ?)", (patient_id, medication_id, 1))

            conn.commit()
            messagebox.showinfo(
                "Prescription", f"Prescription has been sent to the patient")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

        finally:
            conn.close()

    def on_patient_select(self, event):
        selected_patient_name = self.patients_combobox.get()
        if selected_patient_name:
            self.selected_patient = next(
                (patient for patient in self.patients if patient[0] == selected_patient_name), None)
        else:
            self.selected_patient = None

    def on_medication_select(self, event):
        selected_index = self.medication_listbox.curselection()
        if selected_index:
            # Incrementing the selected_index by 1 to match the medication ID in the database
            medication_id = selected_index[0] + 1
            self.selected_medication = (
                self.medication_listbox.get(selected_index[0]), medication_id)
        else:
            self.selected_medication = None

    def open_registration_window(self):
        self.registration_window = tk.Toplevel(self.root)
        self.registration_window.title("Registration")

        # Entry variables for registration
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()

        # Registration form
        tk.Label(self.registration_window, text="First Name:").grid(
            row=0, column=0, sticky="w")
        self.first_name_entry = tk.Entry(
            self.registration_window, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=0, column=1)

        tk.Label(self.registration_window, text="Last Name:").grid(
            row=1, column=0, sticky="w")
        self.last_name_entry = tk.Entry(
            self.registration_window, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=1, column=1)

        tk.Label(self.registration_window, text="Date of Birth:").grid(
            row=2, column=0, sticky="w")
        self.dob_entry = tk.Entry(
            self.registration_window, textvariable=self.dob_var)
        self.dob_entry.grid(row=2, column=1)

        tk.Label(self.registration_window, text="Email:").grid(
            row=3, column=0, sticky="w")
        self.email_entry = tk.Entry(
            self.registration_window, textvariable=self.email_var)
        self.email_entry.grid(row=3, column=1)

        tk.Label(self.registration_window, text="Password:").grid(
            row=4, column=0, sticky="w")
        self.password_entry = tk.Entry(
            self.registration_window, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=4, column=1)

        tk.Button(self.registration_window, text="Register",
                  command=self.register_patient).grid(row=6, columnspan=2)

    def register_patient(self):
        # Get user input
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        dob = self.dob_var.get()
        email = self.email_var.get()
        password = self.password_var.get()

        # Validate user input
        if not (first_name and last_name and dob and email and password):
            messagebox.showerror("Error", "Please fill in all fields.")
            return

        # Insert into Person table
        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Person (firstname, familyname, dateofbirth) VALUES (?, ?, ?)",
                           (first_name, last_name, dob))
            person_id = cursor.lastrowid  # Get the last inserted row id

            conn.commit()

        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"Error inserting into Person table: {e}")
            return

        # Insert into Patient table
        try:
            cursor.execute("INSERT INTO Patient (idperson) VALUES (?)",
                           (person_id,))
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"Error inserting into Patient table: {e}")
            return

        # Insert into Credentials table
        try:
            cursor.execute("INSERT INTO Credentials (email, password, user_type, person_id) VALUES (?, ?, ?, ?)",
                           (email, password, "patient", person_id))
            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"Error inserting into Credentials table: {e}")
            return

        try:
            # Associate the registered patient with the doctor
            self.add_patient_to_doctor(person_id)
            messagebox.showinfo("Success", "Patient registration successful!")
            self.registration_window.destroy()  # Close registration window

        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"Error associating patient with doctor: {e}")
            return

    def add_patient_to_doctor(self, patient_id):
        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()

            # Associate the patient with the doctor
            cursor.execute(
                "INSERT INTO DoctorPatient (iddoctor, idpatient) VALUES (?, ?)", (self.doctor_id, patient_id))

            conn.commit()

        except sqlite3.Error as e:
            print("Database error:", e)

        finally:
            conn.close()


if __name__ == "__main__":
    doctor_main_page = DoctorMainPage(1)
    doctor_main_page.run()
