import os
import pandas as pd
from selenium import webdriver
from selenium.webdriver.firefox.options import Options

#browse Ebay WITHOUT the API to find MTG cards that are listed as in-demand

def search_ebay_items(keywords, max_price):
    options = Options()
    options.add_argument('-headless')
    driver = webdriver.Firefox(options=options)
    base_url = f'https://www.ebay.com/sch/i.html?_nkw={keywords}'

    try:
        driver.get(base_url)
        items = driver.find_elements_by_css_selector('li.s-item')

        for item in items:
            title_element = item.find_element_by_css_selector('h3.s-item__title')
            title = title_element.text.strip()

            price_element = item.find_element_by_css_selector('span.s-item__price')
            price_text = price_element.text.strip()
            price = float(price_text.replace('$', ''))
            
            if price < max_price:
                url_element = item.find_element_by_css_selector('a.s-item__link')
                url = url_element.get_attribute('href')
                print(f'{title} - Price: {price_text} - URL: {url}')

    except Exception as e:
        print('Error occurred:', e)

    finally:
        driver.quit()

if __name__ == '__main__':
    excel_file_path = r'G:\weekly code hyperfocus\EbayFinder\monthly.xlsx'
    try:
        df = pd.read_excel(excel_file_path)
    except Exception as e:
        print('Error reading the Excel file:', e)
        exit()

    if 'newprice' not in df.columns:
        print('Column "newprice" not found in the Excel file.')
        exit()

    for index, row in df.iterrows():
        card_name = row['Card Name']
        new_price = row['newprice']
        search_ebay_items(card_name, new_price)
