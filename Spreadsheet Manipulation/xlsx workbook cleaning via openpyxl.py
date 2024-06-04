import openpyxl
import tkinter as tk
from tkinter import filedialog

def trim_and_normalize(file_path):
    try:
        
        workbook = openpyxl.load_workbook(file_path)
        sheet = workbook.active

        
        column_b = sheet['B']
        for cell in column_b:
            if cell.value:
                cell.value = cell.value.strip()
                cell.value = cell.value.title()  

        
        workbook.save(file_path)
        print("Trailing spaces trimmed and capitals normalized successfully.")

    except Exception as e:
        print("An error occurred:", str(e))

def select_file():
    root = tk.Tk()
    root.withdraw()  

    file_path = filedialog.askopenfilename(filetypes=[("Excel Files", "*.xlsx")])
    if file_path:
        trim_and_normalize(file_path)

if __name__ == "__main__":
    select_file()
