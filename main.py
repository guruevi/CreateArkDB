import json
import os
import re

from pymongo import MongoClient

# Setup MongoDB connection
mongo_client = MongoClient('mongodb://ansible:S%25Rqs5mECnd3%5ES@nsc-docker1:27017/ansible')
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

# Regex to find
string1 = "Intel(R) Core(TM) i7-9700 CPU @ 3.00GHz" # Find i7-9700
string2 = "Intel(R) Core(TM) i5-12500 CPU" # Find i5-12500
string3 = "Intel(R) Xeon(R) Gold 5215 Processor" # Find 5215
regex = re.compile(r"(?:i\d-\d{4,5}|\d{4})")

# Match regex to string
match1 = regex.search(string1)
match2 = regex.search(string2)
match3 = regex.search(string3)
