import argparse
import requests
import pandas as pd
from io import StringIO
from pymongo import MongoClient
from datetime import datetime

from payloads import payload_paranal, payload_lasilla, payload_apex

def request_and_load_to_mongodb(api_url, payload, db_name,all_in_db = False,location = None):
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
    if all_in_db == True:
        if location == 'paranal': df['location'] = 0
        elif location == 'lasilla': df['location'] = 1
        elif location == 'apex': df['location'] = 2
        else: pass
            
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
    parser.add_argument('site', choices=['paranal', 'lasilla','apex','all_in_db'], help='Choose the site (paranal, lasilla, or APEX, or all)')
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
    elif args.site == 'all_in_db': 
        db_name = 'meteo_db'
        api_url_paranal = "http://archive.eso.org/wdb/wdb/asm/meteo_paranal/query"
        api_url_lasilla = "http://archive.eso.org/wdb/wdb/asm/meteo_lasilla/query"
        api_url_apex = 'http://archive.eso.org/wdb/wdb/asm/meteo_apex/query'
    else : pass

    year_range = get_year_range(args.start_year, args.end_year)
    print('Init range: ', year_range[0])
    print('Final range: ', year_range[-1])

    # iterating according to the periods
    if args.site != 'all_in_db':
        for period in year_range:
            payload['start_date'] = period
            print("=" * 40)
            print(f"{period}\n")
            request_and_load_to_mongodb(api_url=api_url, payload=payload, db_name=db_name)
        print("*" * 50, '\n')
        print("Done!")
    
    else :
        for period in year_range:
            payload_paranal['start_date'] = period
            payload_lasilla['start_date'] = period
            payload_apex['start_date'] = period
            print("=" * 40)
            print(f"{period}\n")
            request_and_load_to_mongodb(api_url=api_url_paranal, payload=payload_paranal, db_name=db_name,
                                        all_in_db=True,location = 'paranal')
            print('paranal done')
            request_and_load_to_mongodb(api_url=api_url_lasilla, payload=payload_lasilla, db_name=db_name,
                                        all_in_db=True,location = 'lasilla')
            print('la silla done')
            request_and_load_to_mongodb(api_url=api_url_apex, payload=payload_apex, db_name=db_name,
                                        all_in_db=True,location = 'apex')
            print('apex done')
        print("*" * 50, '\n')
        print("Done!")
