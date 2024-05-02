from tkinter import Button, messagebox

from main_page import MainPage, sqlite3
from main_page import messagebox


class PatientMainPage(MainPage):
    def __init__(self, patient_id):
        super().__init__("patient")
        self.patient_id = patient_id
        self.buy_button = Button(
            self.root, text="Buy Medication", command=self.buy_drugs)
        self.buy_button.pack(pady=5)

        self.prescription_button = Button(
            self.root, text="View Prescription History", command=self.view_prescription_history)
        self.prescription_button.pack(pady=5)

    def buy_drugs(self):
        selected_medication = self.medication_listbox.curselection()
        if not selected_medication:
            messagebox.showerror("Error", "Please select a medication to buy.")
            return

        medication_name = self.medication_listbox.get(selected_medication)
        try:
            conn = sqlite3.connect("pharmacydatabase.db")
            cursor = conn.cursor()
            cursor.execute(
                "SELECT id_medicine FROM Medicine WHERE Med_name=?", (medication_name,))
            medication_id = cursor.fetchone()

            if medication_id:
                cursor.execute(
                    "INSERT INTO PatientMedication (idpatient, id_medicine) VALUES (?, ?)",
                    (self.patient_id, medication_id[0])
                )
                conn.commit()
                messagebox.showinfo(
                    "Success", f"You have purchased {medication_name}.")
            else:
                messagebox.showerror(
                    "Error", "Selected medication not found.")

        except sqlite3.Error as e:
            messagebox.showerror("Error", f"Database error: {e}")

        finally:
            conn.close()

    def view_prescription_history(self):
        print("Viewing prescription history...")
