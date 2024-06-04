from selenium import webdriver
import csv

base_url = "https://download.bls.gov/pub/time.series/ap/"
data_url = base_url + "ap.data.3.Food"
series_url = base_url + "ap.series"
data_csv_filename = "food_data.csv"
series_csv_filename = "ap_series.csv"


options = webdriver.ChromeOptions()
options.add_argument('--headless')  
driver = webdriver.Chrome(options=options)


driver.get(data_url)


data_page_source = driver.page_source


driver.get(series_url)


series_page_source = driver.page_source


driver.quit()


data_lines = data_page_source.splitlines()


with open(data_csv_filename, 'w', newline='') as data_csv_file:
    csv_writer = csv.writer(data_csv_file)
    for line in data_lines:
        csv_writer.writerow([field.strip() for field in line.split('\t')])

print(f"Data downloaded and saved as '{data_csv_filename}'")


series_lines = series_page_source.splitlines()


with open(series_csv_filename, 'w', newline='') as series_csv_file:
    csv_writer = csv.writer(series_csv_file)
    for line in series_lines:
        csv_writer.writerow([field.strip() for field in line.split('\t')])

print(f"Series data downloaded and saved as '{series_csv_filename}'")
