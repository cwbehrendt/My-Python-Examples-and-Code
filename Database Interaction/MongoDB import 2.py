import os
import pandas as pd
from pymongo import MongoClient
import shutil

#another example of importing data to MongoDB via python

def import_csv_to_mongodb(csv_file, mongodb_uri, database_name, collection_name):
    
    df = pd.read_csv(csv_file)

    
    client = MongoClient(mongodb_uri)
    db = client[database_name]
    collection = db[collection_name]

    
    records = df.to_dict(orient='records')

    
    collection.insert_many(records, ordered=False)

    
    client.close()

def move_file_to_archive(src_path, archive_path):
    
    shutil.move(src_path, os.path.join(archive_path, os.path.basename(src_path)))

def main():
    csv_directory = r'G:\weekly code hyperfocus\PriceHistoryScraper'
    archive_directory = r'G:\weekly code hyperfocus\PriceHistoryScraper\archive'
    mongodb_uri = 'mongodb://localhost:27017/'  
    database_name = 'priceHistory'       
    collection_name = 'prices'   

    
    csv_files = [file for file in os.listdir(csv_directory) if file.endswith('.csv')]

    
    for csv_file in csv_files:
        csv_path = os.path.join(csv_directory, csv_file)
        import_csv_to_mongodb(csv_path, mongodb_uri, database_name, collection_name)
        move_file_to_archive(csv_path, archive_directory)
        print(f"Processed and moved: {csv_file}")

if __name__ == "__main__":
    main()
