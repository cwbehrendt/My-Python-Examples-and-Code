import re
import time
import csv
from datetime import datetime, timedelta
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup

#another webscraping example

url = "https://www.tcgplayer.com/product/499292/magic-universes-beyond-the-lord-of-the-rings-tales-of-middle-earth-anduril-flame-of-the-west?xid=pi6a54087f-462a-44ce-b47b-669703cafd99&page=1&Language=English"


driver = webdriver.Chrome()


driver.get(url)


wait = WebDriverWait(driver, 20)
button = wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.charts-item:nth-child(4)')))


button.click()


time.sleep(1)


page_source = driver.page_source


driver.quit()


soup = BeautifulSoup(page_source, 'html.parser')


product_name_element = soup.find('span', {'class': 'lastcrumb', 'data-testid': 'lnkProductDetailsPage', 'data-v-829c873e': ''})
set_name_element = soup.find('span', {'data-testid': 'lblProductDetailsSetName'})


product_name = product_name_element.text.strip() if product_name_element else ""
set_name = set_name_element.text.strip() if set_name_element else ""


sanitized_product_name = re.sub(r'[\\/*?:"<>|]', '_', product_name)


table_element = soup.find('table', {'role': 'region', 'aria-live': 'polite', 'data-v-d8f9e48a': ''})


if table_element:
    print("The <table> element with the specified attributes is present on the page.")

    
    table_data = []
    for row in table_element.find_all('tr'):
        row_data = [cell.get_text(strip=True) for cell in row.find_all(['th', 'td'])]
        table_data.append(row_data)

    
    formatted_data = []
    for i in range(1, len(table_data)):
        date_range, price = table_data[i][0], table_data[i][1]
        start_date, end_date = date_range.split(" to ")
        current_date = datetime.strptime(start_date, "%m/%d")
        end_date = datetime.strptime(end_date, "%m/%d")
        while current_date <= end_date:
            year = datetime.now().year if current_date.year == datetime.now().year else datetime.now().year - 1
            formatted_date = current_date.replace(year=year).strftime("%m/%d/%Y")
            if price.strip():  
                price_value = "Normal" if price == "Normal" else price
                formatted_data.append([formatted_date, sanitized_product_name, set_name, price_value])
            current_date += timedelta(days=1)

    
    current_date_str = datetime.now().strftime("%Y%m%d_%H%M%S")
    file_name = f"{sanitized_product_name} ({current_date_str}).csv"
    file_path = r"G:\weekly code hyperfocus\PriceHistoryScraper\\" + file_name
    with open(file_path, 'w', newline='') as csvfile:
        csv_writer = csv.writer(csvfile)
        csv_writer.writerow(["Date", "Product Name", "Set Name", "Price"])
        csv_writer.writerows(formatted_data)

    print("Formatted table data has been saved to", file_path)

    
    earliest_january_date = None
    with open(file_path, 'r', newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)  
        for row in csv_reader:
            date_str = row[0]
            date = datetime.strptime(date_str, "%m/%d/%Y")
            if date.month == 1:
                earliest_january_date = date
                break

    if earliest_january_date:
        with open(file_path, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            header = next(csv_reader)
            updated_data = []
            adjust_year = False  
            for row in csv_reader:
                date_str = row[0]
                date = datetime.strptime(date_str, "%m/%d/%Y")
                if date == earliest_january_date:
                    adjust_year = True
                if adjust_year:
                    year = datetime.now().year if date.year == datetime.now().year else datetime.now().year - 1
                    date = date.replace(year=year + 1)
                    row[0] = date.strftime("%m/%d/%Y")
                updated_data.append(row)

        with open(file_path, 'w', newline='') as csvfile:
            csv_writer = csv.writer(csvfile)
            csv_writer.writerow(header)
            csv_writer.writerows(updated_data)

        print("Year incremented for dates after the earliest date in January in the CSV.")
    else:
        print("No January date found in the CSV. Year not adjusted.")
else:
    print("The <table> element with the specified attributes is not present on the page.")
