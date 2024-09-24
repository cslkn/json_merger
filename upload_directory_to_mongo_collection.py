import os
import json
from pymongo import MongoClient

def upload_json_files_to_mongo(directory_path, mongo_uri, db_name, collection_name):
    # Connect to MongoDB
    client = MongoClient(mongo_uri)
    db = client[db_name]
    collection = db[collection_name]

    # Iterate over all files in the directory
    for filename in os.listdir(directory_path):
        if filename.endswith('.json'):
            file_path = os.path.join(directory_path, filename)
            with open(file_path, 'r') as file:
                data = json.load(file)
                collection.insert_one(data)
                print(f"Uploaded {filename} to MongoDB")

current_directory = os.path.dirname(os.path.abspath(__file__))
directory_path = os.path.join(current_directory, 'match_info_events')
mongo_uri = 'mongodb+srv://csulkin:wlUApjuSkuJLKEht@cluster0.bwqag.mongodb.net/'
db_name = 'match_data'
collection_name = 'match_info_events'

upload_json_files_to_mongo(directory_path, mongo_uri, db_name, collection_name)