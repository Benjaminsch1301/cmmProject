import requests
import pandas as pd
import yaml
from io import StringIO
from pymongo import MongoClient
from datetime import datetime
from payloads import payload_paranal, payload_lasilla, payload_apex

def request(api_url,payload):
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
    
    return first_line

def request_to_sample(first_line,map_features_int_location ,location_idx, idx =0):
    df = StringIO(first_line.decode('utf-8'))
    df = pd.read_csv(df)

    print('DF created, DF size: ', df.shape)

    if not all(col in df.columns for col in map_features_int_location.keys()):
        raise ValueError("Columns in 'map_features_int_location' are not present in DataFrame")

    df = df.set_index('Date time')
    df = df[list(map_features_int_location.keys())]

    all_samples = []
    for i in range(len(df)):
        for j in range(len(df.columns)):
            
            sample = {
                    "idx": int(idx),
                    "time": str(df.index[i]) ,
                    "node_features": float(df.iloc[i,j]),
                    "type_index": int(map_features_int_location[df.columns[j]]),
                    "spatial_index": int(location_idx),
                }
            all_samples.append(sample)
            
            idx +=1

            
    print('Total samples inserted in this batch: ', len(all_samples))

    return idx, all_samples

def request_and_load_to_mongodb(config:dict, map_features_int:dict, idx : int = 0):
    
    client = MongoClient("mongodb://localhost:27017/")
    db = client[config['db_name']]
    collection = db[config['collection_name']]

    for location in config.keys():
        print('-----',location,'-----')
        api_url = config[location]['api_url']
        payload = config[location]['payload']
        location_idx = config[location]['location_idx']

        map_features_int_location = map_features_int[location]

        # request to endpoint
        first_line = request(api_url,payload)
        idx, all_samples = request_to_sample(first_line,map_features_int_location ,location_idx, idx =idx)

        # Connection to local mongodb
        print(all_samples[0])
        
        collection.insert_many(all_samples)
        print(f"Data inserted into mongodb successfully for {location}!!\n")

    client.close()
    
    return idx 

def get_year_range(start_year, end_year):
    year_list = []
    for year in range(start_year, end_year + 1):
        start_date = datetime(year, 1, 1)
        end_date = datetime(year + 1, 1, 1) if year < end_year else datetime(end_year + 1, 1, 1)
        year_range_str = f"{start_date.strftime('%Y-%m-%d')}..{end_date.strftime('%Y-%m-%d')}"
        year_list.append(year_range_str)
    return year_list

def test():
    with open('yaml/config_download.yaml','r') as f:
        config  = yaml.safe_load(f)
    with open('yaml/map_features_int.yaml','r') as f:
        map_features_int  = yaml.safe_load(f)

    year_range = ['2023-01-01..2023-01-05',
                  '2023-06-01..2023-06-05',
                  '2024-01-01..2024-01-05',
                  ] # YYYY-MM-DD
    
    idx = 0 
    for period_request in year_range:
        
        print('='*100,'\n')
        print('Period: ',period_request)

        payload_paranal['start_date'] = period_request
        payload_apex['start_date'] = period_request
        payload_lasilla['start_date'] = period_request

        config['apex']['payload'] = payload_apex
        config['lasilla']['payload'] = payload_lasilla
        config['paranal']['payload'] = payload_paranal

        idx = request_and_load_to_mongodb(config= config, map_features_int = map_features_int, idx =idx)
        print('last index sample: ', idx)

def download_all():

    with open('yaml/config_download.yaml','r') as f:
        config  = yaml.safe_load(f)
    with open('yaml/map_features_int.yaml','r') as f:
        map_features_int  = yaml.safe_load(f)

    year_range = get_year_range(config['start_year'], config['end_year'])
    print('Init range: ', year_range[0])
    print('Final range: ', year_range[-1])

    idx = 0 
    for period_request in year_range:
        
        print('='*100,'\n')
        print('Period: ',period_request)

        payload_paranal['start_date'] = period_request
        payload_apex['start_date'] = period_request
        payload_lasilla['start_date'] = period_request

        config['apex']['payload'] = payload_apex
        config['lasilla']['payload'] = payload_lasilla
        config['paranal']['payload'] = payload_paranal

        idx = request_and_load_to_mongodb(config = config,map_features_int = map_features_int, idx =idx)
        print('last index sample: ', idx)

if __name__ == '__main__':
    test()
    # download_all()