# packages 
import argparse
import pandas as pd
import numpy as np
import yaml

from pymongo import MongoClient

numeric_cols_paranal = [
    'Air Temperature at 2m [C]',
    'Air Temperature at 30m [C]',
    'Air Temperature at ground [C]',
    'Air Temperature below VLT [C]',
    'Air Temperature instantaneous below VLT [C]',
    'Air Temperature instantanous at 2m [C]',
    'Air Temperature instantanous at 30m [C]',
    'Air Temperature instantanous at ground [C]',
    'Dew Temperature at 2m [C]',
    'Dew Temperature at 30m [C]',
    'Dew Temperature below VLT [C]',
    'Dew Temperature instantanous at 2m [C]',
    'Dew Temperature instantanous below VLT [C]',
    'Dew Temperature istantaneous at 30m [C]',
    'Humidity instantanous at 2m [%]',
    'Humidity instantanous at 30m [%]',
    'Humidity instantanous below VLT [%]',
    'Rain intensity below VLT [%]',
    'Rain intensity instantanous [%]',
    'Relative Humidity at 2m [%]',
    'Relative Humidity at 30m [%]',
    'Relative Humidity below VLT [%]',
    'Wind Direction at 10m (0/360) [deg]',
    'Wind Direction at 10m (180/-180) [deg]',
    'Wind Direction at 30m (0/360) [deg]',
    'Wind Direction at 30m (180/-180) [deg]',
    'Wind Direction instantanous at 10m [deg]',
    'Wind Direction instantanous at 30m [deg]',
    'Wind Speed U at 20m [m/s]',
    'Wind Speed U instantanous at 20m [m/s]',
    'Wind Speed V at 20m [m/s]',
    'Wind Speed V instantanous at 20m [m/s]',
    'Wind Speed W at 20m [m/s]',
    'Wind Speed W instantanous at 20m [m/s]',
    'Wind Speed at 10m [m/s]',
    'Wind Speed at 30m [m/s]',
    'Wind Speed instantanous at 10m [m/s]',
    'Wind Speed instantanous at 30m [m/s]'
 ]

numeric_cols_lasilla = [
    'Ambient Temperature at 30m [C]', 
    'Ambient Temperature at 2m [C]', 
    'Ambient Temperature at ground [C]', 
    'Dew Temperature at 2m [C]', 
    'Relative Humidity at 2m [%]', 
    'Wind Direction at 30m [deg]', 
    'Wind Direction at 10m [deg]', 
    'Wind Speed at 30m [m/s]', 
    'Wind Speed at 10m [m/s]'
    ]

numeric_cols_apex = [
    'Dew Point [C]',
    'Humidity [%]',
    'Temperature [C]',
    'Wind Direction [deg]',
    'Wind Speed [m/s]'
 ]

def get_normal_coef(numeric_cols,db_name):
    client = MongoClient("mongodb://localhost:27017/")
    db = client[db_name] 
    collection = db[db_name]
    with open('yaml/map_features_int.yaml','r') as f:
        map_features_int = yaml.safe_load(f)

    mean_list = []
    std_list = []
    if db_name == 'meteo_paranal':
        location = 0
    elif db_name == 'meteo_lasilla':
        location = 1
    elif db_name == 'meteo_apex':
        location = 2

    for feature in numeric_cols:

        df = pd.DataFrame(list(collection.find({}, {feature: 1, "_id": 0})))

        std = float(df.iloc[:,0].std())
        mean = float(df.iloc[:,0].mean())
        
        int_feature = map_features_int[location][feature]

        std_list.append((int_feature,std))
        mean_list.append((int_feature,mean))

    client.close()
        
    return dict([('mean',dict(mean_list)),('std',dict(std_list))])

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download data from La Silla, Paranal or APEX.')
    parser.add_argument('site', choices=['paranal', 'lasilla','apex','all'], help='Choose the location (paranal, lasilla, apex or all)')
    args = parser.parse_args()

    if args.site == 'paranal':
        dictionary_coef_paranal = get_normal_coef(numeric_cols_paranal,db_name = "meteo_paranal" )
        with open("normal_coef_paranal.yaml","w") as file:
            yaml.dump(dictionary_coef_paranal,file)
        print('Normal coeficients for paranal saved!')

    if args.site == 'lasilla':
        dictionary_coef_lasilla = get_normal_coef(numeric_cols_lasilla,db_name = "meteo_lasilla" )
        with open("normal_coef_lasilla.yaml","w") as file:
            yaml.dump(dictionary_coef_lasilla,file)
        print('Normal coeficients for la silla saved!')

    if args.site == 'apex':
        dictionary_coef_apex = get_normal_coef(numeric_cols_apex,db_name = "meteo_apex" )
        with open("normal_coef_apex.yaml","w") as file:
            yaml.dump(dictionary_coef_apex,file)
        print('Normal coeficients for APEX saved!')

    elif args.site == 'all':

        dictionary_coef_paranal = get_normal_coef(numeric_cols_paranal,db_name = "meteo_paranal" )
        dictionary_coef_lasilla = get_normal_coef(numeric_cols_lasilla,db_name = "meteo_lasilla" )
        dictionary_coef_apex = get_normal_coef(numeric_cols_apex,db_name = "meteo_apex" )

        # all_norm_coef = {'paranal':dictionary_coef_paranal, 
        #                  'lasilla': dictionary_coef_lasilla, 
        #                  'apex': dictionary_coef_apex}

        all_norm_coef = {0:dictionary_coef_paranal, 
                         1: dictionary_coef_lasilla, 
                         2: dictionary_coef_apex}
        
        with open("normal_coef_all.yaml","w") as file:
            yaml.dump(all_norm_coef,file)
        print('Normal coeficients for APEX saved!')
