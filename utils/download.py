import argparse
import requests
import pandas as pd
from io import StringIO
from pymongo import MongoClient
from datetime import datetime

import sys
sys.path.append('/Users/ben_rss/Documents/CMM_2024/cmmProject/')

from utils.payloads import payload_paranal
from utils.payloads import payload_lasilla
from utils.payloads import payload_apex 


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
    print("Dataframe shape: ", df.shape)
    print("Data in DF")
    
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


def get_year_range(start_year, end_year):
    year_list = []
    for year in range(start_year, end_year + 1):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) if year < end_year else datetime(end_year + 1, 1, 1)
        year_range_str = f"{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')}"
        year_list.append(year_range_str)
    return year_list


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download data from La Silla, Paranal or APEX.')
    parser.add_argument('site', choices=['paranal', 'lasilla','apex'], help='Choose the site (paranal, lasilla, or APEX)')
    parser.add_argument('--start_year', type=int, default=1991, help='Start year for data retrieval')
    parser.add_argument('--end_year', type=int, default=2024, help='End year for data retrieval')
    args = parser.parse_args()

    if args.site == 'paranal':
        db_name = "meteo_paranal"
        api_url = "http://archive.eso.org/wdb/wdb/asm/meteo_paranal/query"
        payload = payload_paranal
    elif args.site == 'lasilla':
        db_name = "meteo_lasilla"
        api_url = "http://archive.eso.org/wdb/wdb/asm/meteo_lasilla/query"
        payload = payload_lasilla
    elif args.site == 'apex': 
        db_name = 'meteo_apex'
        api_url = 'http://archive.eso.org/wdb/wdb/asm/meteo_apex/query'
        payload = payload_apex 

    year_range = get_year_range(args.start_year, args.end_year)
    print('Init range: ', year_range[0])
    print('Final range: ', year_range[-1])

    # iterating according to the periods
    for period in year_range:
        payload['start_date'] = period
        print("=" * 40)
        print(f"{period}\n")
        request_and_load_to_mongodb(api_url=api_url, payload=payload, db_name=db_name)
    print("*" * 50, '\n')
    print("Done!")
