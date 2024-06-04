import csv
import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup

#scrapes URL for information on MTG cards

url = 'https://www.mtgstocks.com/analytics/mostplayed'

firefox_options = Options()
firefox_options.add_argument('-headless')

driver = webdriver.Firefox(options=firefox_options)

def fetch_page_content():
    try:
        driver.get(url)
        driver.implicitly_wait(30)

        page_source = driver.page_source
        return page_source
    except Exception as e:
        print(f"Error occurred while fetching the page: {e}")
        return None

def close_driver():
    driver.quit()

def parse_content(page_source):
    soup = BeautifulSoup(page_source, 'html.parser')

    headers_to_find = ['Legacy', 'Vintage', 'Modern', 'Standard', 'Pioneer', 'Pauper']

    for header in headers_to_find:
        header_tag = soup.find('h4', string=header)
        if not header_tag:
            print(f"Failed to find the table with header '{header}' on the webpage.")
            continue

        table = header_tag.find_next('table', {'class': 'table table-striped table-sm'})
        if not table:
            print(f"Failed to find the table with header '{header}' on the webpage.")
            continue

        data = []
        headers = [cell.text.strip() for cell in table.find_all('th')]

        headers = [header for header in headers if not header.isdigit()]

        rows = table.find_all('tr')
        for idx, row in enumerate(rows):
            if idx == 0:
                continue

            cells = row.find_all('td')
            row_data = [cell.text.strip() for cell in cells]
            data.append(row_data)

        csv_file_path = fr'G:\weekly code hyperfocus\mostplayeddump\{header.lower()}.csv'

        with open(csv_file_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Name', 'Price', 'Copies'] + headers)  
            writer.writerows(data)

        print(f"Data from Table '{header}' has been scraped and saved to: {csv_file_path}")

max_attempts = 3
attempts = 1

while attempts <= max_attempts:
    print(f"Attempting to scrape the page - Attempt #{attempts}")
    page_source = fetch_page_content()
    if page_source:
        parse_content(page_source)
        break
    attempts += 1
    print("Retrying in 10 seconds...")
    time.sleep(10)

if attempts > max_attempts:
    print(f"Failed to scrape the page after {max_attempts} attempts.")

close_driver()
