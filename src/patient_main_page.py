# Pharmacy Management System - Patient Main Page
from tkinter import Toplevel, Listbox, Scrollbar, Button
# Importing required modules from the main_page script
from main_page import MainPage, sqlite3
from main_page import messagebox

class PatientMainPage(MainPage): # Subclass of MainPage specifically for patient users : Inheritance Object-Oriented Concept used 
    def __init__(self, patient_id):
        super().__init__("patient") # Calling the constructor of the superclass
        self.root.configure(bg='lightgreen')  # Change la couleur de fond en vert clair
        self.patient_id = patient_id # Storing the patient ID
        # Button for buying medication
        self.buy_button = Button(
            self.root, text="Buy Medication", command=self.buy_drugs, bg='green', fg = 'White')
        self.buy_button.pack(pady=5)
        # Button for viewing prescription history
        self.prescription_button = Button(
            self.root, text="View Prescription History", command=self.view_prescription_history,bg='green', fg = 'White')
        self.prescription_button.pack(pady=5)

    def buy_drugs(self): # Function to buy medication
        selected_medication_index = self.medication_listbox.curselection()
        if not selected_medication_index: # Check if medication is selected
            messagebox.showerror("Error", "Please select a medication to buy.")
            return
        medication_name = self.medication_listbox.get(selected_medication_index[0])
        try: # Connect to DB
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            # Get medication details including ID and content_quantity
            cursor.execute(
                "SELECT id_medicine, content_quantity FROM Medicine WHERE Med_name=?", (medication_name,))
            medication_details = cursor.fetchone()
            if medication_details:
                medication_id, content_quantity = medication_details
                if content_quantity > 0:
                    # Insert the purchase record into PatientMedication table
                    cursor.execute("INSERT INTO PatientMedication (idpatient, id_medicine) VALUES (?, ?)",
                                   (self.patient_id, medication_id))
                    # Update the content_quantity of the medication in the Medicine table
                    cursor.execute("UPDATE Medicine SET content_quantity = content_quantity - 1 WHERE id_medicine=?",
                                   (medication_id,))
                    conn.commit()
                    messagebox.showinfo("Success", f"You have purchased {
                                        medication_name}.")
                    # Refresh the medication list after purchase
                    self.populate_medication_list()
                else: # Error Message
                    messagebox.showerror(
                        "Error", f"{medication_name} is out of stock.")
            else: # Error Message
                messagebox.showerror("Error", "Selected medication not found.")
        except sqlite3.Error as e: # Error Message
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            conn.close()

    def view_prescription_history(self): # Function to view prescription history
        prescription_window = Toplevel(self.root)
        prescription_window.title("Prescription History")
        try: # Connect to DB
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            # Query to retrieve medication name and quantity for which the patient has a prescription
            cursor.execute("""
                SELECT Medicine.Med_name, Prescription.quantity
                FROM Prescription
                INNER JOIN Medicine ON Prescription.id_medicine = Medicine.id_medicine
                WHERE Prescription.idpatient = ?""", (self.patient_id,))
            prescriptions = cursor.fetchall()
            # Display prescriptions in a listbox
            scrollbar = Scrollbar(prescription_window)
            scrollbar.pack(side="right", fill="y")
            prescription_listbox = Listbox(
                prescription_window, yscrollcommand=scrollbar.set)
            for prescription in prescriptions:
                prescription_listbox.insert(
                    "end", f"{prescription[0]} - Quantity: {prescription[1]}")
            prescription_listbox.pack(side="left", fill="both", expand=True)
            scrollbar.config(command=prescription_listbox.yview)
        except sqlite3.Error as e: # Error Message
            messagebox.showerror("Error", f"Database error: {e}")
        finally:
            conn.close()

if __name__ == "__main__": # Create a PatientMainPage instance with patient ID 1 and run the application
    PatientMainPage(1).run()