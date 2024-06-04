import os
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
import re
import time
import random
from requests.exceptions import ConnectTimeout

#scrapes URL and converts to JSON

def extract_dates(html_content):
    date_pattern = re.compile(r'\b\d{2}/\d{2}/\d{4}\b')
    dates = date_pattern.findall(html_content)
    return dates


def scrape_and_filter_dates(url):
    retry_count = 3
    for attempt in range(retry_count):
        try:
            response = requests.get(url, timeout=(5, 15))  
            response.raise_for_status()  

            html_content = response.text
            all_dates = extract_dates(html_content)

            
            current_date = datetime.now()
            three_years_ago = current_date - timedelta(days=3*365)
            filtered_dates = [date for date in all_dates if datetime.strptime(date, '%m/%d/%Y') >= three_years_ago]

            
            return list(set(filtered_dates))

        except ConnectTimeout as e:
            print(f"Attempt {attempt + 1} failed to connect to {url}: {e}")
            if attempt < retry_count - 1:
                delay = random.uniform(5, 7)
                print(f"Retrying in {delay:.2f} seconds...")
                time.sleep(delay)
            else:
                print(f"Max retries exceeded. Exiting.")
                return []

        except requests.RequestException as e:
            print(f"Failed to scrape dates from {url}: {e}")
            return []


def download_beef_data(second_url):
    time.sleep(random.uniform(5, 7))  
    response = requests.get(second_url)
    try:
        data = response.json()
        if isinstance(data, list):
            
            data = data[0]
    except json.JSONDecodeError:
        print(f"Failed to parse JSON from the response for {second_url}. Skipping...")
        return None

    return data


def convert_json_to_csv(json_file_path, csv_file_path):
    try:
        
        with open(json_file_path, 'r') as json_file:
            data = json.load(json_file)

        if isinstance(data, list):
            
            data = data[0]

        
        results = data.get('results', [])

        
        df = pd.DataFrame(results)

        
        if os.path.exists(csv_file_path):
            df.to_csv(csv_file_path, mode='a', header=False, index=False)
        else:
            df.to_csv(csv_file_path, index=False)

        print(f"Conversion successful. Data appended to CSV at: {csv_file_path}")

    except Exception as e:
        print(f"Error converting JSON to DataFrame and saving as CSV: {e}")


def main():
    
    url1 = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports/2460"
    filtered_dates = scrape_and_filter_dates(url1)

    if not filtered_dates:
        print("No valid dates found. Exiting.")
        return

    
    second_url_base = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports/2460?q=report_date={}&allSections=true"
    
    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    csv_file_path = os.path.join(desktop_path, "tee_hee_output.csv")

    
    for report_date in filtered_dates:
        if report_date:
            
            second_url = second_url_base.format(report_date)

            
            beef_data = download_beef_data(second_url)

            if beef_data is not None:
                
                json_file_path = os.path.join(desktop_path, f"tee_hee_{report_date.replace('/', '-')}.json")

                with open(json_file_path, "w") as json_file:
                    json.dump(beef_data, json_file, indent=2)

                print(f"JSON file saved to {json_file_path}")

                
                convert_json_to_csv(json_file_path, csv_file_path)

    print("Processing complete.")


if __name__ == "__main__":
    main()
