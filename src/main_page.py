# Pharmacy Management System - Main Page
from tkinter import Tk, Label, Frame, Scrollbar, Listbox, END, messagebox
import sqlite3

class MainPage: # Main page class for displaying medication list
    def __init__(self, user_type):
        # Initialize Tkinter window
        self.root = Tk()
        self.root.title(f"{user_type.capitalize()} Main Page")
        # Frame to contain the medication list and scrollbar
        self.medication_frame = Frame(self.root)
        self.medication_frame.pack(pady=10)
        # Label for the medication list
        self.medication_label = Label(
            self.medication_frame, text="Medication List:")
        self.medication_label.pack(side="left")
        # Listbox to display the medication list
        self.medication_listbox = Listbox(
            self.medication_frame, width=40, height=10)
        self.medication_listbox.pack(side="left", fill="both", expand=True)
        # Scrollbar for the medication listbox
        scrollbar = Scrollbar(self.medication_frame, orient="vertical")
        scrollbar.config(command=self.medication_listbox.yview)
        scrollbar.pack(side="right", fill="y")
        self.medication_listbox.config(yscrollcommand=scrollbar.set)
        # Populate the medication listbox with data from the database
        self.populate_medication_list()

    def run(self): # Start the Tkinter event loop
        self.root.mainloop() 

    def populate_medication_list(self):
        try: # Connect to the SQLite database
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            # Clear the existing list of medications
            self.medication_listbox.delete(0, END)
            # Retrieve the list of medications from the database
            cursor.execute("SELECT Med_name FROM Medicine")
            medications = cursor.fetchall()
            # Populate the medication listbox with the retrieved medications
            for medication in medications:
                self.medication_listbox.insert(END, medication[0])
        except sqlite3.Error as e: # Display an error message if there's a database error
            messagebox.showerror("Error", f"Database error: {e}")
        finally: # Close the database connection
            conn.close()