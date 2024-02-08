import torch
from torch.utils.data import Dataset, DataLoader
from pymongo import MongoClient
import pandas as pd
import random
import yaml
import sys
sys.path.append('/Users/ben_rss/Documents/CMM_2024/cmmProject/')

from utils.utils_columns import numeric_cols_using
with open('normal_coef_paranal.yaml','r') as f:
    normal_coef_paranal = yaml.safe_load(f)
with open('normal_coef_lasilla.yaml','r') as f:
    normal_coef_lasilla = yaml.safe_load(f)
with open('normal_coef_apex.yaml','r') as f:
    normal_coef_apex = yaml.safe_load(f)

class ObsMeteoDataset(Dataset):
    def __init__(self, norm_coef, collection):

        self.collection = collection
        self.mean_dict = norm_coef['mean']
        self.std_dict = norm_coef['std']
        self.features = list(self.mean_dict.keys())

        self.ids = [elem['_id'] for elem in list(self.collection.find({}, {'_id': 1}))]
        random.shuffle(self.ids)

        self.dataset_size = len(self.ids)

    def __len__(self):
        return self.dataset_size

    def __getitem__(self, idx):

        id = self.ids[idx]

        data_id = self.collection.find_one({'_id': id})

        # self.ids = [doc_id for doc_id in self.ids if doc_id !=id] # deleting ids to avoid duplicates in training
        
        ## using normal coef
        id_list= []
        for feature in self.features:
            id_list.append( (data_id[feature]-self.mean_dict[feature])/self.std_dict[feature]  )
            
        data_id_tensor = torch.tensor(id_list,dtype=torch.float32)
        
        return data_id_tensor,data_id['Date time']
    


client = MongoClient("mongodb://localhost:27017/")

## Paranal
db_name = "meteo_paranal" 
db = client[db_name] 
collection_paranal = db[db_name]
dataset_apex = ObsMeteoDataset( norm_coef = normal_coef_paranal,collection = collection_paranal)
dataloader_paranal = DataLoader(dataset_apex, batch_size=32, shuffle=True, num_workers=0)


## La Silla
db_name = "meteo_lasilla" 
db = client[db_name] 
collection_lasilla = db[db_name]
dataset_lasilla = ObsMeteoDataset( norm_coef = normal_coef_lasilla,collection = collection_lasilla)
dataloader_lasilla = DataLoader(dataset_lasilla, batch_size=32, shuffle=True, num_workers=0)


## APEX
db_name = "meteo_apex" 
db = client[db_name] 
collection_apex = db[db_name]
dataset_apex = ObsMeteoDataset( norm_coef = normal_coef_apex,collection = collection_apex)
dataloader_apex = DataLoader(dataset_apex, batch_size=32, shuffle=True, num_workers=0)


print('Paranal')
i = 0
for batch,date_time in dataloader_paranal:
    print(batch,date_time)
    i+=1
    if i == 2: break


print('*'*50)
print('\nLaSilla')

i = 0

for batch,date_time in dataloader_lasilla:
    print(batch,date_time)
    i+=1
    if i == 2: break


print('*'*50)
print('\nAPEX')

i = 0

for batch,date_time in dataloader_apex:
    print(batch,date_time)
    i+=1
    if i == 2: break

client.close()