import requests
import pandas as pd
from io import StringIO
from pymongo import MongoClient
from datetime import datetime

db_name = "meteo_lasilla" # meteo_paranal_test, meteo_paranal, meteo_lasilla

client = MongoClient("mongodb://localhost:27017/")
db = client[db_name] # meteo_paranal_test
collection = db[db_name]


print('Total samples: ',collection.count_documents({})) # total samples
print('Last sample: \n',collection.find_one(sort=[("_id", 1)]))# last one 



## samples per year
pipeline = [
    {   # it extracts the year from Date time
        "$project": {
            "year": {"$year": {"$dateFromString": {"dateString": "$Date time"}}},
        }
    },
    {   # grouping by year and sum per sample 
        "$group": {
            "_id": "$year",
            "count": {"$sum": 1},
        }
    },
    {   
        "$sort": {"_id": 1}  # Sort by year in ascending order
    }
]
result = list(collection.aggregate(pipeline))
for entry in result:
    print(f"Year: {entry['_id']}, Count: {entry['count']}")