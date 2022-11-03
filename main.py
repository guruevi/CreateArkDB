import json
import os

from pymongo import MongoClient

# Setup MongoDB connection
mongo_client = MongoClient('mongodb://user:pass@server:27017/')
db = mongo_client['ansible']
collection = db['intel_ark']


def find_files(path_to_json):
    # Walk through all files in path_to_json
    for root, dirs, files in os.walk(path_to_json):
        for file in files:
            if file.endswith('.json'):
                # Open JSON file
                with open(os.path.join(root, file)) as json_file:
                    data = json.load(json_file)
                    # Insert JSON data into MongoDB
                    # Upsert is used to update existing data
                    if 'arkid' in data:
                        data["_id"] = data["arkid"]
                        # Strip Qn' from string and add 20
                        print(data)
                        # Convert string to int
                        year = data["Essentials"]["BornOnDate"][3:]
                        if int(year) > 80:
                            year = "19" + year
                        else:
                            year = "20" + year
                        data["Essentials"]["BornYear"] = year
                        collection.update_one({'_id': data['arkid']}, {'$set': data}, upsert=True)
                    else:
                        print(data)


if __name__ == '__main__':
    find_files("./items")