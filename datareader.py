import yaml
import random
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from pymongo import MongoClient
from datetime import datetime
from tqdm import trange, tqdm
from AGG.extended_typing import ContinuousTimeGraphSample

class ObsMeteoDataset(Dataset):
    def __init__(self, config ):
        self.lazy_loaded = False
        self.config = config
        self.len = config['len_train']

    def lazy_load_db(self):
        self.client = MongoClient(self.config['host'])
        self.collection = self.client[self.config['db_name']][self.config['collection_train']]
        self.lazy_loaded = True

    @staticmethod
    def collate_fn(samples):
        return samples

    def __len__(self):
        return self.len

    def __getitem__(self, idx:ContinuousTimeGraphSample)-> ContinuousTimeGraphSample  :
        if self.lazy_loaded == False:
            self.lazy_load_db()
        
        sample = self.collection.find_one({"id": idx},{'_id':0,'id':0})

        if "attention_mask" not in sample or len(sample["attention_mask"]) == 0:
            sample["time"] = torch.tensor(sample["time"], dtype=torch.float)
            sample["attention_mask"] = sample["time"].unsqueeze(-1).T < sample[
                "time"
            ].unsqueeze(-1)
        sample = ContinuousTimeGraphSample(**sample)
        return sample

def test_dataloader():
    with open('config.yaml','r') as f:
        config = yaml.safe_load(f)   
    obs_dataset = ObsMeteoDataset( config=config)
    dataloader = DataLoader(obs_dataset, batch_size=32, shuffle=True, num_workers=0, collate_fn=ObsMeteoDataset.collate_fn)

    print('*'*50)
    i = 0
    for batch in dataloader:
        print(batch)
        i+=1
        if i == 2: break

if __name__ == '__main__':
    test_dataloader()
