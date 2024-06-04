import openpyxl
import tkinter as tk
from tkinter import filedialog
import os


def pad_numbers(number):
    return str(number).zfill(13)


root = tk.Tk()
root.withdraw()  


file_path = filedialog.askopenfilename(title="Select Excel file", filetypes=[("Excel files", "*.xlsx *.xls")])

if file_path:
    
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active

    
    column_f = sheet['F']

    
    for cell in column_f:
        if isinstance(cell.value, (int, float)):
            cell.value = pad_numbers(int(cell.value))

    
    output_directory = os.path.dirname(file_path)
    output_file_path = os.path.join(output_directory, "padded_numbers.xlsx")

    
    workbook.save(output_file_path)
    print(f"Modified data saved to {output_file_path}")
else:
    print("No file selected.")


root.destroy()
