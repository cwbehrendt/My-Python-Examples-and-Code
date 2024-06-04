import os
import pandas as pd
from pymongo import MongoClient
from datetime import datetime
import time


#imports data from webscrape into MongoDB

time.sleep(300)


mongodb_uri = "mongodb://localhost:27017/"
database_name = "MostPlayed"


csv_directory = "G:/weekly code hyperfocus/mostplayeddump"

def import_csv_to_mongodb(csv_path, db, collection_name, day, month, year):
    
    df = pd.read_csv(csv_path)
    
    
    df['day'] = day
    df['month'] = month
    df['year'] = year
    
    
    data = df.to_dict(orient='records')
    
    
    collection = db[collection_name]
    collection.insert_many(data)
    print(f"Successfully imported {len(data)} records to collection '{collection_name}'.")

def main():
    
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    
    
    current_date = datetime.now()
    day = current_date.day
    month = current_date.month
    year = current_date.year
    
    
    for filename in os.listdir(csv_directory):
        if filename.endswith(".csv"):
            collection_name = os.path.splitext(filename)[0]  
            csv_path = os.path.join(csv_directory, filename)
            
            import_csv_to_mongodb(csv_path, db, collection_name, day, month, year)

    client.close()

if __name__ == "__main__":
    main()
