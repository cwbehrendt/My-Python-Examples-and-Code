import os
import requests
import json



def get_report_date(second_url):
    response = requests.get(second_url)
    data = response.json()
    report_date = data['results'][0]['report_date']
    return report_date

def download_beef_data(first_url):
    response = requests.get(first_url)
    beef_data = response.json()
    return beef_data

def main():
    second_url = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports/2460"
    first_url_template = "https://mpr.datamart.ams.usda.gov/services/v1.1/reports/2460?q=report_date={}&allSections=true"
    
    report_date = get_report_date(second_url)

    first_url = first_url_template.format(report_date)

    beef_data = download_beef_data(first_url)

    desktop_path = os.path.join(os.path.expanduser("~"), "Desktop")
    json_file_path = os.path.join(desktop_path, "tee_hee.json")

    with open(json_file_path, "w") as json_file:
        json.dump(beef_data, json_file, indent=2)

    print(f"JSON file saved to {json_file_path}")

if __name__ == "__main__":
    main()
