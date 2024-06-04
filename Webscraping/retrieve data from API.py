import requests

#fetches the names of ALL MTG card sets from scryfall (card db) API

def get_all_sets():
    url = "https://api.scryfall.com/sets"
    all_sets = []

    while url:
        response = requests.get(url)
        data = response.json()

        all_sets.extend(data['data'])

        if data['has_more']:
            url = data['next_page']
        else:
            url = None

    return all_sets

def save_sets_to_file(sets_list, filename):
    import json
    with open(filename, 'w') as f:
        json.dump(sets_list, f, indent=2)

if __name__ == "__main__":
    all_sets = get_all_sets()
    save_sets_to_file(all_sets, "sets_output.json")
    print("Sets data saved to 'sets_output.json'")
