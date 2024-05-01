import tkinter as tk
from tkinter import messagebox, ttk
import sqlite3


class LoginPortal:

    def __init__(self, root):
        self.root = root
        self.root.title("Login Portal")
        self.root.geometry("300x200")  # Set the size of the window

        # Connect to the database
        self.conn = sqlite3.connect('pharmacydatabase.db')
        self.c = self.conn.cursor()

        # Create labels
        tk.Label(root, text="email:").grid(
            row=0, column=0, padx=5, pady=5, sticky=tk.E)
        tk.Label(root, text="Password:").grid(
            row=1, column=0, padx=5, pady=5, sticky=tk.E)

        # Create entry fields
        self.email_entry = tk.Entry(root)
        self.email_entry.grid(row=0, column=1, padx=5, pady=5)
        self.password_entry = tk.Entry(root, show="*")  # Mask the password
        self.password_entry.grid(row=1, column=1, padx=5, pady=5)

        # Create login button
        self.login_button = tk.Button(root, text="Login", command=self.login)
        self.login_button.grid(row=3, column=0, columnspan=2, padx=5, pady=10)

        # Create register button
        self.register_button = tk.Button(
            root, text="Register", command=self.open_registration_window)
        self.register_button.grid(
            row=4, column=0, columnspan=2, padx=5, pady=10)

    def login(self):
        # Functionality for login button
        email = self.email_entry.get()
        password = self.password_entry.get()
        # Check for empty fields
        if not email or not password:
            messagebox.showerror(
                "Error", "Please enter both email and password.")
            return
        # Authenticate user
        user = self.authenticate_user(email, password)

        if user:
            tk.messagebox.showinfo("Login Successful", f"Welcome, {user[5]}")
            if user[3] == "patient":
                print("patient")
            elif user[3] == "doctor":
                pass
            elif user[3] == "pharmacist":
                pass
        else:
            tk.messagebox.showerror(
                "Login Failed", "Incorrect email or password")

    def authenticate_user(self, email, password):
        # Authenticate the user based on credentials and fetch additional person information
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
        self.registration_window = tk.Toplevel(self.root)
        self.registration_window.title("Registration")

        # Entry variables for registration
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.dob_var = tk.StringVar()
        self.email_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.user_type_var = tk.StringVar()
        self.user_types = ["patient", "doctor", "pharmacist"]

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

        tk.Label(self.registration_window, text="User Type:").grid(
            row=5, column=0, sticky="w")
        self.user_type_menu = ttk.Combobox(
            self.registration_window, textvariable=self.user_type_var, values=self.user_types)
        self.user_type_menu.grid(row=5, column=1)

        tk.Button(self.registration_window, text="Register",
                  command=self.register).grid(row=6, columnspan=2)

    def register(self):
        # Get user input
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        dob = self.dob_var.get()
        email = self.email_var.get()
        password = self.password_var.get()
        user_type = self.user_type_menu.get()

        # Validate user input
        if not (first_name and last_name and dob and email and password and user_type):
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
            conn.close()

        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"Error inserting into Person table: {e}")
            return

        # Determine which table to insert into based on user_type
        if user_type == "patient":
            table_name = "Patient"
        elif user_type == "doctor":
            table_name = "Doctor"
        elif user_type == "pharmacist":
            table_name = "Pharmacist"
        else:
            messagebox.showerror("Error", "Invalid user type.")
            return

        # Insert into the corresponding user type table
        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()

            cursor.execute(f"INSERT INTO {table_name} (idperson) VALUES (?)",
                           (person_id,))

            conn.commit()
        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Error inserting into {
                                 table_name} table: {e}")
            return
        finally:
            conn.close()

        # Insert into Credentials table
        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()

            cursor.execute("INSERT INTO Credentials (email, password, user_type, person_id) VALUES (?, ?, ?, ?)",
                           (email, password, user_type, person_id))

            conn.commit()
            conn.close()
        except sqlite3.Error as e:
            messagebox.showerror(
                "Error", f"Error inserting into Credentials table: {e}")
            return

        messagebox.showinfo("Success", "Registration successful!")

        # Optionally, close the registration window after successful registration
        self.registration_window.destroy()


def main():
    # Create and run the login portal
    root = tk.Tk()
    root.geometry("400x300")
    app = LoginPortal(root)
    root.mainloop()


if __name__ == "__main__":
    main()
