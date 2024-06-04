import tkinter as tk
from tkinter import filedialog
import csv
import re

def process_csv(file_path):
    output_lines = []

    with open(file_path, newline='', encoding='utf-8-sig') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            processed_row = [re.sub(r'\r|\n', ' ', cell) for cell in row]
            processed_row = [cell.replace('â€™', "'") for cell in processed_row]
            output_lines.append(processed_row)

    with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(output_lines)

def select_file():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '*.csv')])
    if file_path:
        process_csv(file_path)
        status_label.config(text="File processed and saved.")

app = tk.Tk()
app.title("CSV Processor")

select_button = tk.Button(app, text="Select CSV File", command=select_file)
select_button.pack(pady=20)

status_label = tk.Label(app, text="")
status_label.pack()

app.mainloop()
