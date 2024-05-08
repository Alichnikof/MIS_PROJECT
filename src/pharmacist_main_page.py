# Pharmacy Management System - Pharmacist Main Page
from tkinter import Button, Label, Frame, Scrollbar, Listbox, END, messagebox, Entry, simpledialog
# Importing required modules from the main_page script
from main_page import MainPage, sqlite3
from main_page import messagebox


# Subclass of MainPage specifically for pharmacist users : Inheritance Object-Oriented Concept used
class PharmacistMainPage(MainPage):
    def __init__(self):
        super().__init__("pharmacist")  # Call superclass constructor
        # Additional UI elements for pharmacist
        # Add Medication Entry and Button
        self.add_medication_entry = Entry(self.root)
        self.add_medication_entry.pack(pady=5)
        self.add_medication_button = Button(
            self.root, text="Add Medication", command=self.add_medication, bg='Green', fg='White')
        self.add_medication_button.pack(pady=5)
        # Add to Stock Button
        self.add_to_stock_button = Button(
            self.root, text="Add to Stock", command=self.add_to_stock, bg='Green', fg='White')
        self.add_to_stock_button.pack(pady=5)
        # Verify Quantity Button
        self.verify_quantity_button = Button(
            self.root, text="Verify Quantity", command=self.verify_quantity, bg='Green', fg='White')
        self.verify_quantity_button.pack(pady=5)

    def add_medication(self):  # Function to add new medication
        medication_name = self.add_medication_entry.get().strip()
        if not medication_name:  # If no medication is written
            messagebox.showerror(
                "Error", "Please enter a medication name.")
            return
        try:  # Connect to DB
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            # Check if the medication already exists
            cursor.execute(
                "SELECT * FROM Medicine WHERE Med_name=?", (medication_name,))
            existing_medication = cursor.fetchone()
            if existing_medication:
                messagebox.showerror(
                    "Error", f"The medication '{medication_name}' already exists.")
                return
            # Insert the new medication into the Medicine table
            cursor.execute(
                "INSERT INTO Medicine (Med_name, content_quantity) VALUES (?, ?)", (medication_name, 0))
            conn.commit()
            # Show success message
            messagebox.showinfo(
                "Success", f"The medication '{medication_name}' has been added.")
            # Clear the entry field after adding medication
            self.add_medication_entry.delete(0, END)
            # Refresh the medication list
            self.populate_medication_list()
        except sqlite3.Error as e:  # Error message
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            conn.close()

    def add_to_stock(self):  # Function to add medication to stock
        # Get the index of the selected medication in the listbox
        selected_medication_index = self.medication_listbox.curselection()
        if not selected_medication_index:  # If no medication selected
            messagebox.showerror(
                "Error", "Please select a medication to add to stock.")
            return
        # Get the name of the selected medication
        medication_name = self.medication_listbox.get(
            selected_medication_index[0])
        # Prompt the user to enter the quantity
        quantity = simpledialog.askinteger(
            "Add to Stock", f"Enter quantity to add for {medication_name}:")
        if quantity is None:
            return  # User clicked cancel or closed the dialog
        try:
            # Connect to the database
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            # Update the quantity of the selected medication in the database
            cursor.execute(
                "UPDATE Medicine SET content_quantity = content_quantity + ? WHERE Med_name = ?",
                (quantity, medication_name)
            )
            conn.commit()
            # Show success message
            messagebox.showinfo(
                "Success", f"{quantity} units of {medication_name} added to the stock.")
        except sqlite3.Error as e:  # Error Message
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            conn.close()

    def verify_quantity(self):  # Function to verify medication quantity
        # Get the index of the selected medication in the listbox
        selected_medication_index = self.medication_listbox.curselection()
        if not selected_medication_index:  # If no medication selected
            messagebox.showerror(
                "Error", "Please select a medication to verify quantity.")
            return
        # Get the name of the selected medication
        medication_name = self.medication_listbox.get(
            selected_medication_index[0])
        try:
            # Connect to the database
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            # Retrieve the quantity of the selected medication from the database
            cursor.execute(
                "SELECT content_quantity FROM Medicine WHERE Med_name = ?",
                (medication_name,)
            )
            quantity = cursor.fetchone()[0]  # Fetch the quantity value
            # Show the quantity in a messagebox
            messagebox.showinfo("Verify Quantity", f"The quantity of {
                                medication_name} is {quantity}.")
        except sqlite3.Error as e:  # Error Message
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            conn.close()


if __name__ == "__main__":  # Create a PharmacistMainPage instance and run the application
    doctor_main_page = PharmacistMainPage()
    doctor_main_page.run()
