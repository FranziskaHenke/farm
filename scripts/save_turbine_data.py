import csv
import json
from datetime import datetime
import pymongo 

client = pymongo.MongoClient("mongodb://root:password@localhost:27017/farm?authSource=admin")
db = client["farm"]
turbine_collection = db["turbines"] 

def create_json(csvFilePath):
    data = []     
    with open(csvFilePath, encoding='utf-8') as f:
        keys = []
        data = []
        csvReader = csv.reader(f)
        for i, row in enumerate(csvReader):
            if(i == 0):
                keys = [r.strip() for r in row]
            elif(i == 1):
                keys = [(keys[i]+ ' '+ k.strip()).strip() for i,k in enumerate(row)]
                keys = list(map(lambda x: x[1]+ " " + str(keys[:x[0]].count(x[1]) + 1) if keys.count(x[1]) > 1 else x[1], enumerate(keys)))
            else:
                # TODO cast string numbers to real numbers
                data.append({keys[i]: r for i,r in enumerate(row)})            
    data = [{k.replace('.', ''): v for k, v in d.items()} for d in data]
    return data

def add_entry_to_json(json, key, value):
    for j in json:
        j[key] = value
    return json

def convert_key_to_timestamp(json, key, format):
    for j in json:
        j[key] = datetime.strptime(j[key], format)
    return json

entries = [
    {'path': './scripts/static_data/turbine_data/Turbine1.csv', 'Turbine': '1'},
    {'path': './scripts/static_data/turbine_data/Turbine2.csv', 'Turbine': '2'}
]
 
# Call the make_json function
for e in entries:
    json = create_json(e['path'])
    json = add_entry_to_json(json, 'Turbine',e['Turbine'])
    json = convert_key_to_timestamp(json, 'Dat/Zeit', '%d.%m.%Y, %H:%M') 
    turbine_collection.insert_many(json)
    print('number of entries in turbine collection:',turbine_collection.count_documents({}))
    
