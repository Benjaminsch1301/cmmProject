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
    norm_coef = yaml.safe_load(f)


## connecting
db_name = "meteo_paranal_test" 

client = MongoClient("mongodb://localhost:27017/")
db = client[db_name] # meteo_paranal_test
collection = db[db_name]

class ObsDataset(Dataset):
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
    


test_paranal_dataset = ObsDataset( norm_coef = norm_coef,collection = collection)


dataloader = DataLoader(test_paranal_dataset, batch_size=32, shuffle=True, num_workers=0)

i = 0
for batch,date_time in dataloader:
    print(batch,date_time)
    i+=1
    if i == 3: break