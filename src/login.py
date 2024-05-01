import tkinter as tk
from tkinter import messagebox
import sqlite3


class LoginPortal:
    def __init__(self, master):
        # Initialize the login portal
        self.master = master
        # Connect to the database
        self.conn = sqlite3.connect('pharmacydatabase.db')
        self.c = self.conn.cursor()
        # Create the Credentials table if it doesn't exist
        self.create_credentials_table()
        # Set up the main window
        self.master.title("Login Portal: Enter Login Credentials")
        # Create GUI elements for the login form
        self.create_login_form()

    def create_credentials_table(self):
        # Create the Credentials table if it doesn't exist
        self.c.execute('''
            CREATE TABLE IF NOT EXISTS Credentials (
                id INTEGER PRIMARY KEY,
                email TEXT UNIQUE,
                password TEXT,
                user_type TEXT,
                FOREIGN KEY (email) REFERENCES Person(email)
            )
        ''')
        self.conn.commit()

    def create_login_form(self):
        # Create labels, entry fields, and login button for the login form
        # Email
        self.label_email = tk.Label(self.master, text="Email:")
        self.label_email.pack()
        self.entry_email = tk.Entry(self.master)
        self.entry_email.pack()
        # Password
        self.label_password = tk.Label(self.master, text="Password:")
        self.label_password.pack()
        self.entry_password = tk.Entry(self.master, show="*")
        self.entry_password.pack()
        # Login
        self.btn_login = tk.Button(
            self.master, text="Login", command=self.handle_login)
        self.btn_login.pack()

    def handle_login(self):
        # Handle the login process
        entered_email = self.entry_email.get()
        entered_password = self.entry_password.get()
        # Check for empty fields
        if not entered_email or not entered_password:
            messagebox.showerror(
                "Error", "Please enter both email and password.")
            return
        # Authenticate user
        user_type = self.authenticate_user(entered_email, entered_password)
        # Open respective window based on user type
        if user_type == "Pharmacist":
            self.open_pharmacist_window()
        elif user_type == "Doctor":
            self.open_doctor_window()
        elif user_type == "Patient":
            self.open_patient_window()
        else:
            messagebox.showerror("Error", "Invalid email or password.")

    def authenticate_user(self, email, password):
        # Authenticate the user based on credentials
        self.c.execute(
            "SELECT user_type FROM Credentials WHERE email=? AND password=?", (email, password))
        user = self.c.fetchone()
        if user:
            return user[0]
        else:
            return None

    def open_pharmacist_window(self):
        # Open the pharmacist window with relevant functionalities
        pharmacist_window = tk.Toplevel(self.master)
        pharmacist_window.title("Pharmacist Window")
        # Add buttons/menu and labels for pharmacist functionalities
        tk.Label(pharmacist_window, text="Pharmacist Dashboard",
                 font=("Arial", 16, 'bold')).pack(pady=20)
        # View Prescriptions button
        tk.Button(pharmacist_window, text="View Prescriptions",
                  command=self.view_prescriptions).pack(pady=5)
        # Manage Medicines button
        tk.Button(pharmacist_window, text="Manage Medicines",
                  command=self.manage_medicines).pack(pady=5)

    def view_prescriptions(self):
        # Functionality for viewing prescriptions
        # You can implement this based on your project requirements
        pass

    def manage_medicines(self):
        # Functionality for managing medicines
        # You can implement this based on your project requirements
        pass

    def open_doctor_window(self):
        # Open the doctor window with relevant functionalities
        doctor_window = tk.Toplevel(self.master)
        doctor_window.title("Doctor Window")
        # Add buttons/menu and labels for doctor functionalities
        tk.Label(doctor_window, text="Doctor Dashboard",
                 font=("Arial", 16, 'bold')).pack(pady=20)
        # View Appointments button
        tk.Button(doctor_window, text="View Appointments",
                  command=self.view_appointments).pack(pady=5)
        # Manage Patients button
        tk.Button(doctor_window, text="Manage Patients",
                  command=self.manage_patients).pack(pady=5)

    def view_appointments(self):
        # Functionality for viewing appointments
        # You can implement this based on your project requirements
        pass

    def manage_patients(self):
        # Functionality for managing patients
        # You can implement this based on your project requirements
        pass

    def open_patient_window(self):
        # Open the patient window with relevant functionalities
        patient_window = tk.Toplevel(self.master)
        patient_window.title("Patient Window")
        # Add buttons/menu and labels for patient functionalities
        tk.Label(patient_window, text="Patient Dashboard",
                 font=("Arial", 16, 'bold')).pack(pady=20)
        # View Appointments button
        tk.Button(patient_window, text="View Appointments",
                  command=self.view_appointments).pack(pady=5)
        # Request Appointment button
        tk.Button(patient_window, text="Request Appointment",
                  command=self.request_appointment).pack(pady=5)

    def request_appointment(self):
        # Functionality for requesting appointment
        # You can implement this based on your project requirements
        pass


def main():
    # Create and run the login portal
    root = tk.Tk()
    root.geometry("400x300")
    app = LoginPortal(root)
    root.mainloop()


if __name__ == "__main__":
    main()
