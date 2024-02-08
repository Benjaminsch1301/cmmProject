# packages 
import argparse
import pandas as pd
import numpy as np
import yaml

from pymongo import MongoClient

import sys
sys.path.append('/Users/ben_rss/Documents/CMM_2024/cmmProject/')

from utils.utils_columns import numeric_cols_using as numeric_cols_paranal

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

    mean_list = []
    std_list = []
    for feature in numeric_cols:
        df = pd.DataFrame(list(collection.find({}, {feature: 1, "_id": 0})))

        std = float(df.iloc[:,0].std())
        mean = float(df.iloc[:,0].mean())
        
        std_list.append((feature,std))
        mean_list.append((feature,mean))

    
    client.close()
        
    return dict([('mean',dict(mean_list)),('std',dict(std_list))])



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Download data from La Silla, Paranal or APEX.')
    parser.add_argument('site', choices=['paranal', 'lasilla','apex','all'], help='Choose the site (paranal, lasilla, apex or all)')
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
        with open("normal_coef_paranal.yaml","w") as file:
            yaml.dump(dictionary_coef_paranal,file)
        print('Normal coeficients for paranal saved!')

        dictionary_coef_lasilla = get_normal_coef(numeric_cols_lasilla,db_name = "meteo_lasilla" )
        with open("normal_coef_lasilla.yaml","w") as file:
            yaml.dump(dictionary_coef_lasilla,file)
        print('Normal coeficients for la silla saved!')
    
        dictionary_coef_apex = get_normal_coef(numeric_cols_apex,db_name = "meteo_apex" )
        with open("normal_coef_apex.yaml","w") as file:
            yaml.dump(dictionary_coef_apex,file)
        print('Normal coeficients for APEX saved!')


