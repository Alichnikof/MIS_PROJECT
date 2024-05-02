from tkinter import Button, Label, Frame, Scrollbar, Listbox, END, messagebox

from main_page import MainPage, messagebox, sqlite3


class DoctorMainPage(MainPage):
    def __init__(self, doctor_id):
        super().__init__("doctor")
        self.doctor_id = doctor_id
        self.selected_patient = None
        self.selected_medication = None
        self.patients = None  # Initialize patients attribute
        self.populate_patients_list()

    def populate_patients_list(self):
        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Person.firstname, Patient.idpatient
                FROM Person
                INNER JOIN DoctorPatient ON Person.idperson = DoctorPatient.idpatient
                INNER JOIN Patient ON DoctorPatient.idpatient = Patient.idpatient
                WHERE DoctorPatient.iddoctor = ?""", (self.doctor_id,))
            self.patients = cursor.fetchall()  # Store patients in attribute

            self.patients_frame = Frame(self.root)
            self.patients_frame.pack(pady=10)
            self.patients_label = Label(
                self.patients_frame, text="Patients List:")
            self.patients_label.pack(side="left")
            self.patients_listbox = Listbox(
                self.patients_frame, width=40, height=10)
            self.patients_listbox.pack(side="left", fill="both", expand=True)
            scrollbar = Scrollbar(self.patients_frame, orient="vertical")
            scrollbar.config(command=self.patients_listbox.yview)
            scrollbar.pack(side="right", fill="y")
            self.patients_listbox.config(yscrollcommand=scrollbar.set)

            for patient in self.patients:
                self.patients_listbox.insert(END, patient[0])

            self.patients_listbox.bind(
                "<<ListboxSelect>>", self.on_patient_select)

        except sqlite3.Error as e:
            print("Database error:", e)

        finally:
            conn.close()

        self.prescribe_button = Button(
            self.root, text="Prescribe Medication", command=self.prescribe_medication)
        self.prescribe_button.pack(pady=5)

        self.medication_listbox.bind(
            "<<ListboxSelect>>", self.on_medication_select)

    def prescribe_medication(self):
        if not self.selected_patient:
            messagebox.showerror("Error", "Please select a patient.")
            return
        if not self.selected_medication:
            messagebox.showerror(
                "Error", "Please select a medication to prescribe.")
            return

        patient_id = self.selected_patient[1]
        medication_id = self.selected_medication[1]

        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT * FROM Prescription WHERE idpatient=? AND id_medicine=?", (patient_id, medication_id))
            existing_prescription = cursor.fetchone()
            if existing_prescription:
                cursor.execute(
                    "UPDATE Prescription SET quantity = quantity + 1 WHERE id_prescription=?", (existing_prescription[0],))
            else:
                cursor.execute(
                    "INSERT INTO Prescription (idpatient, id_medicine, quantity) VALUES (?, ?, ?)", (patient_id, medication_id, 1))

            conn.commit()
            messagebox.showinfo(
                "Prescription", f"Prescription added for Patient ID {patient_id} for Medication ID {medication_id}.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

        finally:
            conn.close()

    def on_patient_select(self, event):
        selected_index = self.patients_listbox.curselection()
        if selected_index:
            self.selected_patient = self.patients[selected_index[0]]
        else:
            self.selected_patient = None

    def on_medication_select(self, event):
        selected_index = self.medication_listbox.curselection()
        if selected_index:
            self.selected_medication = (
                self.medication_listbox.get(selected_index[0]), selected_index[0])
        else:
            self.selected_medication = None


if __name__ == "__main__":
    doctor_main_page = DoctorMainPage(1)
    doctor_main_page.run()
