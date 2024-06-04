import tkinter as tk
from tkinter import filedialog
import pandas as pd
import googlemaps
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


API_KEY = 'API KEY REDACTED'


def calculate_distance(city1, city2, gmaps):
    try:
        base_url = "https://maps.googleapis.com/maps/api/directions/json"
        params = {
            "origin": city1,
            "destination": city2,
            "mode": "driving",
            "key": API_KEY,
        }
        response = requests.get(base_url, params=params, verify=False)
        data = response.json()
        
        if "routes" in data and data["routes"]:
            distance = data["routes"][0]["legs"][0]["distance"]["text"]
            return distance
        else:
            return "Error: Unable to calculate distance"
    except Exception as e:
        return "Error: " + str(e)


def process_file():
    file_path = filedialog.askopenfilename(title="Select a CSV file")
    if file_path:
        try:
            gmaps = googlemaps.Client(key=API_KEY)
            df = pd.read_csv(file_path)
            if 'city 1' in df.columns and 'city 2' in df.columns:
                df['distance'] = df.apply(lambda row: calculate_distance(row['city 1'], row['city 2'], gmaps), axis=1)
                df.to_csv(file_path, index=False)
                print("Distances calculated and saved to the file.")
            else:
                print("Error: The file does not contain 'city 1' and 'city 2' columns.")
        except Exception as e:
            print(f"Error: {str(e)}")
    else:
        print("No file selected.")


root = tk.Tk()
root.withdraw()  


process_file()
