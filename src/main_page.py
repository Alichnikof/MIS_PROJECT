from tkinter import Tk, Label, Button, Frame, Scrollbar, Listbox, END, messagebox


class MainPage:
    def __init__(self, user_type):
        self.root = Tk()
        # Set window title based on user type
        self.root.title(f"{user_type.capitalize()} Main Page")
        # Common UI elements
        Label(self.root, text=f"Welcome, {user_type.capitalize()}!").pack()

    def run(self):
        self.root.mainloop()


class PatientMainPage(MainPage):
    def __init__(self):
        super().__init__("patient")  # Call superclass constructor
        # Additional UI elements for patient
        self.medication_frame = Frame(self.root)
        self.medication_frame.pack(pady=10)
        self.medication_label = Label(self.medication_frame, text="Medication List:")
        self.medication_label.pack(side="left")
        self.medication_listbox = Listbox(self.medication_frame, width=40, height=10)
        self.medication_listbox.pack(side="left", fill="both", expand=True)
        self.populate_medication_list()  # Populate medication list
        scrollbar = Scrollbar(self.medication_frame, orient="vertical")
        scrollbar.config(command=self.medication_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.medication_listbox.config(yscrollcommand=scrollbar.set)
        # Buy Button
        self.buy_button = Button(self.root, text="Buy Medication", command=self.buy_drugs)
        self.buy_button.pack(pady=5)
        # Prescription Button
        self.prescription_button = Button(self.root, text="View Prescription History", command=self.view_prescription_history)
        self.prescription_button.pack(pady=5)

    def populate_medication_list(self):
        # In a real scenario, you would fetch medication from the database
        medications = ["Medication 1", "Medication 2","Medication 3", "Medication 4", "Medication 5"]
        for medication in medications:
            self.medication_listbox.insert(END, medication)

    def buy_drugs(self):
        selected_medication = self.medication_listbox.curselection()
        if not selected_medication:
            messagebox.showerror("Error", "Please select a medication to buy.")
            return
        selected_medication_index = selected_medication[0]
        medication = self.medication_listbox.get(selected_medication_index)
        messagebox.showinfo("Purchase", f"You have purchased {medication}.")

    def view_prescription_history(self):
        print("Viewing prescription history...")


class DoctorMainPage(MainPage):
    def __init__(self):
        super().__init__("doctor")  # Call superclass constructor
        # Patients List
        self.patients_frame = Frame(self.root)
        self.patients_frame.pack(pady=10)
        self.patients_label = Label(self.patients_frame, text="Patients List:")
        self.patients_label.pack(side="left")
        self.patients_listbox = Listbox(self.patients_frame, width=40, height=10)
        self.patients_listbox.pack(side="left", fill="both", expand=True)
        self.populate_patients_list() # Populate patients list
        scrollbar = Scrollbar(self.patients_frame, orient="vertical")
        scrollbar.config(command=self.patients_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.patients_listbox.config(yscrollcommand=scrollbar.set)
        # Medication List
        self.medication_frame = Frame(self.root)
        self.medication_frame.pack(pady=10)
        self.medication_label = Label(self.medication_frame, text="Medication List:")
        self.medication_label.pack(side="left")
        self.medication_listbox = Listbox(self.medication_frame, width=40, height=10)
        self.medication_listbox.pack(side="left", fill="both", expand=True)
        self.populate_medication_list() # Populate medication list
        scrollbar = Scrollbar(self.medication_frame, orient="vertical")
        scrollbar.config(command=self.medication_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.medication_listbox.config(yscrollcommand=scrollbar.set)
        # Prescribe Button
        self.prescribe_button = Button(self.root, text="Prescribe Medication", command=self.prescribe_medication)
        self.prescribe_button.pack(pady=5)

    def populate_patients_list(self):
        # In a real scenario, you would fetch patients from the database
        patients = ["Patient 1", "Patient 2","Patient 3", "Patient 4", "Patient 5"]
        for patient in patients:
            self.patients_listbox.insert(END, patient)

    def populate_medication_list(self):
        # In a real scenario, you would fetch medication from the database
        medications = ["Medication 1", "Medication 2","Medication 3", "Medication 4", "Medication 5"]
        for medication in medications:
            self.medication_listbox.insert(END, medication)

    def prescribe_medication(self):
        selected_patient_index = self.patients_listbox.curselection()
        selected_medication_index = self.medication_listbox.curselection()
        if not selected_patient_index or not selected_medication_index:
            messagebox.showerror("Error", "Please select a patient and medication to prescribe.")
            return
        patient = self.patients_listbox.get(selected_patient_index[0])
        medication = self.medication_listbox.get(selected_medication_index[0])
        # Reset selections
        self.patients_listbox.selection_clear(0, END)
        self.medication_listbox.selection_clear(0, END)
        # Display prescription message after clearing selections
        messagebox.showinfo("Prescription", f"You have prescribed {medication} to {patient}.")


class PharmacistMainPage(MainPage):
    def __init__(self):
        super().__init__("pharmacist")  # Call superclass constructor
        # Additional UI elements for pharmacist
        # Medication List
        self.medication_frame = Frame(self.root)
        self.medication_frame.pack(pady=10)
        self.medication_label = Label(self.medication_frame, text="Medication List:")
        self.medication_label.pack(side="left")
        self.medication_listbox = Listbox(self.medication_frame, width=40, height=10, selectmode="single")
        self.medication_listbox.pack(side="left", fill="both", expand=True)
        self.populate_medication_list() # Populate medication list
        scrollbar = Scrollbar(self.medication_frame, orient="vertical")
        scrollbar.config(command=self.medication_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.medication_listbox.config(yscrollcommand=scrollbar.set)
        # Add to Stock Button
        self.add_to_stock_button = Button(self.root, text="Add to Stock", command=self.add_to_stock)
        self.add_to_stock_button.pack(pady=5)
        # Verify Quantity Button
        self.verify_quantity_button = Button(self.root, text="Verify Quantity", command=self.verify_quantity)
        self.verify_quantity_button.pack(pady=5)
        # Patients List
        self.patients_frame = Frame(self.root)
        self.patients_frame.pack(pady=10)
        self.patients_label = Label(self.patients_frame, text="Patients List:")
        self.patients_label.pack(side="left")
        self.patients_listbox = Listbox(self.patients_frame, width=40, height=5, selectmode="single")
        self.patients_listbox.pack(side="left", fill="both", expand=True)
        self.populate_patients_list() # Populate patients list
        scrollbar = Scrollbar(self.patients_frame, orient="vertical")
        scrollbar.config(command=self.patients_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.patients_listbox.config(yscrollcommand=scrollbar.set)
        # Doctors List
        self.doctors_frame = Frame(self.root)
        self.doctors_frame.pack(pady=10)
        self.doctors_label = Label(self.doctors_frame, text="Doctors List:")
        self.doctors_label.pack(side="left")
        self.doctors_listbox = Listbox(self.doctors_frame, width=40, height=5, selectmode="single")
        self.doctors_listbox.pack(side="left", fill="both", expand=True)
        self.populate_doctors_list()  # Populate doctors list
        scrollbar = Scrollbar(self.doctors_frame, orient="vertical")
        scrollbar.config(command=self.doctors_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.doctors_listbox.config(yscrollcommand=scrollbar.set)

    def populate_medication_list(self):
        # In a real scenario, you would fetch medication from the database
        medications = ["Medication 1", "Medication 2","Medication 3", "Medication 4", "Medication 5"]
        for medication in medications:
            self.medication_listbox.insert(END, medication)

    def add_to_stock(self):
        selected_medication_index = self.medication_listbox.curselection()
        if not selected_medication_index:
            messagebox.showerror("Error", "Please select a medication to add to stock.")
            return
        medication = self.medication_listbox.get(selected_medication_index[0])
        messagebox.showinfo("Add to Stock", f"You have added {medication} to stock.")

    def verify_quantity(self):
        selected_medication_index = self.medication_listbox.curselection()
        if not selected_medication_index:
            messagebox.showerror(
                "Error", "Please select a medication to verify quantity.")
            return
        medication = self.medication_listbox.get(selected_medication_index[0])
        messagebox.showinfo("Verify Quantity", f"The quantity of {medication} is sufficient.")

    def populate_patients_list(self):
        # In a real scenario, you would fetch patients from the database
        patients = ["Patient 1", "Patient 2","Patient 3", "Patient 4", "Patient 5"]
        for patient in patients:
            self.patients_listbox.insert(END, patient)

    def populate_doctors_list(self):
        # In a real scenario, you would fetch doctors from the database
        doctors = ["Doctor 1", "Doctor 2", "Doctor 3", "Doctor 4", "Doctor 5"]
        for doctor in doctors:
            self.doctors_listbox.insert(END, doctor)

main_page = PharmacistMainPage()
main_page.run()