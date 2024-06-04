import pandas as pd


df = pd.read_csv(r"FILEPATH REDACTED CAUSE COMPANY INFORMATION WAS HERE, ENJOY THIS MESSAGE")


def extract_dates(section_df):
    date = section_df["Time:Week Ending"].iloc[0].split()[-1]
    section_df["Week_Ending_Date"] = date
    return section_df


df = df.groupby("Time:Week Ending").apply(extract_dates).reset_index(drop=True)


df.to_csv("modified_file.csv", index=False)
