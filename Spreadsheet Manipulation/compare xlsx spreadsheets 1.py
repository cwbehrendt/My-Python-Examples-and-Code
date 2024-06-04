import pandas as pd

#simple code block to compare my MTG card inventory against a list of in-demand cards to find ones worth money

csv_file_0 = "G:/weekly code hyperfocus/EbayFinder/table_0.csv"
csv_file_1 = "G:/weekly code hyperfocus/EbayFinder/table_1.csv"
excel_file = "G:/weekly code hyperfocus/EbayFinder/AllCards.xlsx"

df_table_0 = pd.read_csv(csv_file_0)
df_table_1 = pd.read_csv(csv_file_1)
df_all_cards = pd.read_excel(excel_file)

cards_in_table_0 = df_table_0['Card']
cards_in_table_1 = df_table_1['Card']
cards_in_all_cards = df_all_cards['Card Name']

unique_cards_in_all_cards = set(cards_in_all_cards)

common_cards_table_0 = cards_in_table_0[cards_in_table_0.isin(unique_cards_in_all_cards)]

common_cards_table_1 = cards_in_table_1[cards_in_table_1.isin(unique_cards_in_all_cards)]

print("Common cards in table_0.csv:")
print(common_cards_table_0)

print("\nCommon cards in table_1.csv:")
print(common_cards_table_1)
