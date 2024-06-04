import pandas as pd

def find_matching_cards():
    # File paths
    allcards_file = r'G:\weekly code hyperfocus\EbayFinder\AllCards.xlsx'
    monthly_file = r'G:\weekly code hyperfocus\EbayFinder\monthly.xlsx'

    try:
        # Read the Excel files into Pandas DataFrames
        allcards_df = pd.read_excel(allcards_file)
        monthly_df = pd.read_excel(monthly_file)

        # Extract the 'Card Name' columns from both DataFrames
        allcards_names = allcards_df['Card Name']
        monthly_names = monthly_df['Card Name']

        # Find matches
        matching_cards = allcards_names[allcards_names.isin(monthly_names)]

        # Display the matches
        print("Matching Cards:")
        print(matching_cards)

    except FileNotFoundError as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    find_matching_cards()
