import requests
from bs4 import BeautifulSoup

#scrapes ingredients

def scrape_ingredients(url):
    
    response = requests.get(url)
    
    
    if response.status_code == 200:
        
        soup = BeautifulSoup(response.text, 'html.parser')

        
        ingredients = []

        
        if 'bhg.com' in url:
            ingredient_elements = soup.find_all('li', class_='ingredient')
            ingredients = [ingredient.get_text(strip=True) for ingredient in ingredient_elements]

        
        elif 'bbcgoodfood.com' in url:
            ingredient_elements = soup.find_all('li', class_='ingredients-list__item')
            ingredients = [ingredient.get_text(strip=True) for ingredient in ingredient_elements]

        return ingredients
    else:
        
        print(f"Failed to retrieve content from {url}. Status code: {response.status_code}")
        return None


url1 = 'https://www.bhg.com/recipe/thin-crust-pepperoni-and-vegetable-pizza/'
url2 = 'https://www.bbcgoodfood.com/recipes/chicken-korma'


ingredients_url1 = scrape_ingredients(url1)
ingredients_url2 = scrape_ingredients(url2)


if ingredients_url1:
    print("Ingredients for Thin Crust Pepperoni and Vegetable Pizza:")
    for ingredient in ingredients_url1:
        print("- " + ingredient)

if ingredients_url2:
    print("\nIngredients for Chicken Korma:")
    for ingredient in ingredients_url2:
        print("- " + ingredient)
