import tkinter as tk
from tkinter import filedialog
import csv

#converts TCGPlayer order spreadsheet to a csv i can use to print labels from

def open_csv_file():
    file_path = filedialog.askopenfilename(filetypes=[("CSV Files", "*.csv")])
    if file_path:
        process_csv(file_path)

def process_csv(file_path):
    field_map = {
        "FirstName": "First Name",
        "LastName": "Last Name",
        "Address1": "Street",
        "PostalCode": "ZIP code"
    }

    with open(file_path, 'r', newline='') as file:
        reader = csv.DictReader(file)
        headers = reader.fieldnames

        
        renamed_headers = [field_map.get(header, header) for header in headers]

        
        data = []
        for row in reader:
            updated_row = {field_map.get(key, key): value for key, value in row.items()}
            data.append(updated_row)

    
    new_file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
    if new_file_path:
        with open(new_file_path, 'w', newline='') as new_file:
            writer = csv.DictWriter(new_file, fieldnames=renamed_headers)
            writer.writeheader()
            writer.writerows(data)
        print("CSV file successfully processed and saved!")


root = tk.Tk()
root.withdraw()  


open_csv_file()
