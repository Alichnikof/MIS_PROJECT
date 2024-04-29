from tkinter import Tk, Label, Button


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
        self.view_history_button = Button(
            self.root, text="View Prescription History", command=self.view_prescription_history)
        self.view_history_button.pack()

    def view_prescription_history(self):
        print("Viewing prescription history...")


class DoctorMainPage(MainPage):
    def __init__(self):
        super().__init__("doctor")  # Call superclass constructor
        # Additional UI elements for doctor
        self.prescribe_medication_button = Button(
            self.root, text="Prescribe Medication", command=self.prescribe_medication)
        self.prescribe_medication_button.pack()

    def prescribe_medication(self):
        print("Prescribing medication...")


class PharmacistMainPage(MainPage):
    def __init__(self):
        super().__init__("pharmacist")  # Call superclass constructor
        # Additional UI elements for pharmacist
        self.fill_prescription_button = Button(
            self.root, text="Fill Prescription", command=self.fill_prescription)
        self.fill_prescription_button.pack()

    def fill_prescription(self):
        print("Filling prescription...")


# Example usage
user_type = "doctor"  # Replace with actual user type
if user_type == "patient":
    main_page = PatientMainPage()
elif user_type == "doctor":
    main_page = DoctorMainPage()
elif user_type == "pharmacist":
    main_page = PharmacistMainPage()

main_page.run()
