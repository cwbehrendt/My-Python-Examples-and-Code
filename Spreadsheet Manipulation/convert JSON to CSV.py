import tkinter as tk
from tkinter import filedialog
import json
import pandas as pd

#literally just converts a JSON to a CSV

def convert_json_to_csv():
    
    file_path = filedialog.askopenfilename(title="Select JSON file", filetypes=[("JSON files", "*.json")])

    if file_path:
        try:
            
            with open(file_path, 'r') as json_file:
                data = json.load(json_file)

            
            rows = []
            for item in data:
                results = item.get('results', [])
                for result in results:
                    row = result.copy()
                    row.update({'reportSection': item.get('reportSection', '')})
                    rows.append(row)

            
            df = pd.DataFrame(rows)

            
            csv_file_path = file_path.replace('.json', '_output.csv')
            df.to_csv(csv_file_path, index=False)

            print(f"Conversion successful. DataFrame saved as CSV at: {csv_file_path}")

        except Exception as e:
            print(f"Error converting JSON to DataFrame and saving as CSV: {e}")


root = tk.Tk()
root.title("JSON to DataFrame Converter")


convert_button = tk.Button(root, text="Convert JSON to DataFrame and Save as CSV", command=convert_json_to_csv)
convert_button.pack(pady=20)


root.mainloop()
