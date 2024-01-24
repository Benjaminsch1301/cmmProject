import requests
import pandas as pd
from io import StringIO
from pymongo import MongoClient
from datetime import datetime

from utils.payloads import  payload_paranal   
from utils.payloads import payload_lasilla 



def request_and_load_to_mongodb(api_url, payload, db_name):
    
    # request to endpoint
    try:
        response = requests.get(api_url, params=payload)
        print("Request status: ", response.status_code)
    except requests.exceptions.RequestException as e:
        print(f"Error in api request: {e}")

    content_lines = response.content.split(b"\n\n")

    # checking the content
    if content_lines:
        first_line = content_lines[0]
    else:
        print("No data received from the api :(")

    # set as a object file 
    csv_data = StringIO(first_line.decode('utf-8'))
    df = pd.read_csv(csv_data)
    print("Dataframe shape: ",df.shape)
    print("Data in DF" )
    # print('memory usage: ',df.memory_usage(deep=True).sum())
    # Connection to local mongodb
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client[db_name]
        collection = db[db_name]
        records = df.to_dict('records')
        collection.insert_many(records)
        print("Data inserted into mongodb successfully!!")
    except Exception as e:
        print(f"Error saving: {e}")
    finally:
        client.close()


def get_year_range(start_year ,end_year ):
    "function which gets year range as a list"
    year_list = []
    for year in range(start_year, end_year + 1):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) if year < end_year else datetime(end_year + 1, 1, 1)
        year_range_str = f"{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')}"
        year_list.append(year_range_str)
    return year_list


year_range_paranal = {'start_year' : 1998,'end_year' :2024}
year_range_lasierra = {'start_year' : 1991,'end_year' : 2024} # 1991

year_range = get_year_range(**year_range_lasierra)
print('Init range: ',year_range[0])
print('Final range',year_range[-1])

# db_name = "meteo_paranal" # meteo_paranal_test, meteo_paranal
# api_url = "http://archive.eso.org/wdb/wdb/asm/meteo_paranal/query"
# payload = payload_paranal 

db_name = "meteo_lasilla"
api_url =  "http://archive.eso.org/wdb/wdb/asm/meteo_lasilla/query"
payload =payload_lasilla


# iterating according to the periods
for period in year_range:
    payload['start_date'] = period
    print("="*40)
    print(f"{period}\n")
    request_and_load_to_mongodb(api_url = api_url , payload = payload, db_name = db_name)
print("*"*50,'\n')
print("Done!")