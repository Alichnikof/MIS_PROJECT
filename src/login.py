# Pharmacy Management System - Login Portal
import re
import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3
# Importing the Patient/Doctor/PharmacistMainPage classes from patient/doctor/pharmacist_main_page scripts
from patient_main_page import PatientMainPage
from doctor_main_page import DoctorMainPage
from pharmacist_main_page import PharmacistMainPage


class LoginPortal:  # Class representing the login portal functionality
    """Represents the login portal of the Pharmacy Management System."""

    def __init__(self, root):
        """Initialize the login portal."""
        self.root = root
        self.root.title("Login Portal")  # Set the title of the window
        self.root.geometry("300x200")  # Set the size of the window
        # Change la couleur de fond en vert clair
        self.root.configure(bg='lightgreen')
        # Connect to the database
        self.conn = sqlite3.connect('pharmacydatabase.db')
        self.c = self.conn.cursor()
        # Create labels fpr email and password
        tk.Label(root, text="email:", bg='lightgreen').grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(root, text="Password:", bg='lightgreen').grid(
            row=2, column=0, padx=5, pady=5, sticky=tk.E)
        # Create a tilte
        self.title_label = tk.Label(root, text="Pharmacy Management System", font=(
            "Arial", 15, "bold"), bg='#34eb43', fg='white')
        self.title_label.grid(row=0, column=0, columnspan=2, pady=10)
        # Create entry fields
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=1, column=1, padx=5, pady=5)
        self.password_entry = tk.Entry(root, show="*")  # Mask the password
        self.password_entry.grid(row=2, column=1, padx=5, pady=5)
        # Create login button
        self.login_button = tk.Button(
            root, text="Login", command=self.login, bg='green', fg='White')
        self.login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)
        # Create register button
        self.register_button = tk.Button(
            root, text="Register", command=self.open_registration_window, bg='green', fg='White')
        self.register_button.grid(
            row=4, column=0, columnspan=2, padx=5, pady=10)

    def validate_email(self, email):
        """Validate email format and disallow certain special characters."""
        if re.match(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$", email):
            if not any(char in email for char in "#!$%&'*+/=?^_`{|}~"):
                return True
        return False

    def login(self):
        """Authenticate the user and perform login."""
        # Functionality for login button
        email = self.email_entry.get()
        password = self.password_entry.get()
        # Check for empty fields
        if not email or not password:  # If no email/password inserted
            messagebox.showerror(
                "Error", "Please enter both email and password.")
            return

        # Validate email format
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        # Authenticate user
        user = self.authenticate_user(email, password)
        if user:
            tk.messagebox.showinfo("Login Successful", f"Welcome, {user[5]}")
            # Patient
            if user[3] == "patient":
                patient_id = user[0]
                patient_main_page = PatientMainPage(patient_id)
                patient_main_page.run()
            # Doctor
            elif user[3] == "doctor":
                doctor_id = user[0]
                doctor_main_page = DoctorMainPage(doctor_id)
                doctor_main_page.run()
            # Pharmacist
            elif user[3] == "pharmacist":
                pharmacist_id = user[0]
                pharmacist_main_page = PharmacistMainPage()
                pharmacist_main_page.run()
        else:  # Error Message
            tk.messagebox.showerror(
                "Login Failed", "Incorrect email or password")

    def authenticate_user(self, email, password):
        """Authenticate the user based on credentials and fetch additional person information."""
        query = """
                SELECT Credentials.*, Person.firstname
                FROM Credentials
                INNER JOIN Person ON Credentials.person_id = Person.idperson
                WHERE Credentials.email=? AND Credentials.password=?
                """
        self.c.execute(query, (email, password))
        user = self.c.fetchone()  # Fetch the first matching row
        if user:
            return user  # Return user details if credentials are correct
        else:
            return None  # Return None if no matching user found

    def open_registration_window(self):
        """Open the registration window."""
        self.registration_window = tk.Toplevel(self.root)
        self.registration_window.title("Registration")
        # Entry variables for registration
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.user_type_var = tk.StringVar()
        self.user_types = ["doctor", "pharmacist"]
        # Registration form
        # Label for First Name Entry
        tk.Label(self.registration_window, text="First Name:").grid(
            row=0, column=0, sticky="w")
        self.first_name_entry = tk.Entry(
            self.registration_window, textvariable=self.first_name_var)
        self.first_name_entry.grid(row=0, column=1)
        # Label for Last Name Entry
        tk.Label(self.registration_window, text="Last Name:").grid(
            row=1, column=0, sticky="w")
        self.last_name_entry = tk.Entry(
            self.registration_window, textvariable=self.last_name_var)
        self.last_name_entry.grid(row=1, column=1)
        # Label for Date of Birth Entry
        tk.Label(self.registration_window, text="Date of Birth:").grid(
            row=2, column=0, sticky="w")
        self.dob_entry = tk.Entry(
            self.registration_window, textvariable=self.dob_var)
        self.dob_entry.grid(row=2, column=1)
        # Label for First Email Entry
        tk.Label(self.registration_window, text="Email:").grid(
            row=3, column=0, sticky="w")
        self.email_entry = tk.Entry(
            self.registration_window, textvariable=self.email_var)
        self.email_entry.grid(row=3, column=1)
        # Label for First Password Entry
        tk.Label(self.registration_window, text="Password:").grid(
            row=4, column=0, sticky="w")
        self.password_entry = tk.Entry(
            self.registration_window, textvariable=self.password_var, show="*")
        self.password_entry.grid(row=4, column=1)
        # Label for User Type Entry
        tk.Label(self.registration_window, text="User Type:").grid(
            row=5, column=0, sticky="w")
        self.user_type_menu = ttk.Combobox(
            self.registration_window, textvariable=self.user_type_var, values=self.user_types)
        self.user_type_menu.grid(row=5, column=1)
        # Register Button
        tk.Button(self.registration_window, text="Register",
                  command=self.register, bg='green', fg='White').grid(row=6, columnspan=2)

    def register(self):
        """Register a new user."""
        # Get user input
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        dob = self.dob_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        user_type = self.user_type_menu.get()
        # Validate user input
        # If no Credentials inserted
        if not (first_name and last_name and dob and email and password and user_type):
            messagebox.showerror("Error", "Please fill in all fields.")
            return
        # Validate email format
        if not self.validate_email(email):
            messagebox.showerror("Error", "Invalid email format.")
            return
        # Insert into Person table
        try:  # Connect to DB
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Person (firstname, familyname, dateofbirth) VALUES (?, ?, ?)",
                           (first_name, last_name, dob))
            person_id = cursor.lastrowid  # Get the last inserted row id
            conn.commit()
            conn.close()
        except sqlite3.Error as e:  # Error Message
            messagebox.showerror(
                "Error", f"Error inserting into Person table: {e}")
            return
        # Determine which table to insert into based on user_type
        if user_type == "doctor":
            table_name = "Doctor"
        elif user_type == "pharmacist":
            table_name = "Pharmacist"
        else:  # Error Message
            messagebox.showerror("Error", "Invalid user type.")
            return
        # Insert into the corresponding user type table
        try:  # Connect to DB
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            cursor.execute(f"INSERT INTO {table_name} (idperson) VALUES (?)",
                           (person_id,))
            conn.commit()
        except sqlite3.Error as e:  # Error Message
            messagebox.showerror("Error", f"Error inserting into {
                                 table_name} table: {e}")
            return
        finally:
            conn.close()
        # Insert into Credentials table
        try:  # Connect to DB
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            cursor.execute("INSERT INTO Credentials (email, password, user_type, person_id) VALUES (?, ?, ?, ?)",
                           (email, password, user_type, person_id))
            conn.commit()
            conn.close()
        except sqlite3.Error as e:  # Error Message
            messagebox.showerror(
                "Error", f"Error inserting into Credentials table: {e}")
            return
        # Success Message
        messagebox.showinfo("Success", "Registration successful!")
        # Optionally, close the registration window after successful registration
        self.registration_window.destroy()


def main():
    # Create and run the login portal
    root = tk.Tk()  # Tkinter root window
    root.geometry("800x300")  # Size Window
    app = LoginPortal(root)  # Create an instance of the LoginPortal class
    root.mainloop()  # Event loop


if __name__ == "__main__":
    main()  # Main call
