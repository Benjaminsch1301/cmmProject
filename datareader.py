import yaml
import random
import numpy as np
import torch
from torch.utils.data import Dataset, DataLoader
from pymongo import MongoClient
from datetime import datetime
from tqdm import trange, tqdm
from AGG.extended_typing import ContinuousTimeGraphSample

with open('int_name_normal_coef.yaml','r') as f:
    int_name_normal_coef = yaml.safe_load(f)

def get_sorted_idx_list(config):
    client = MongoClient("mongodb://localhost:27017/")
    db = client[config['db_name']] # meteo_paranal_test
    collection = db[config['collection_pure_samples']]
    ids = [elem['idx'] for elem in collection.find({}, {'idx': 1}).sort("time", 1)]
    return ids

def get_graph_sample_idx(context_len, stride, idx_list, selection_size):
    targets = set(random.sample(idx_list, int(selection_size * len(idx_list))))  
    print('Total targets: ',len(targets))
    train_nodes = [k for k in idx_list if k not in targets] # O(1) targets is save it as by hash functions
    N = len(train_nodes)
    print('Total train nodes: ', N)
    windows = []
    idx_indices = {idx: i for i, idx in enumerate(idx_list)}
    k=0
    graph_samples = dict()
    print('Creating indexes of nodes...')
    for i in trange(0, N, stride):
        max_idx = min(i + context_len, N) 
        window = train_nodes[i:max_idx] 
        if len(window)==context_len: 
            windows.append(window) 
            first_element_window = idx_indices[window[0]]
            last_element_window = idx_indices[window[-1]]
            for target in targets : 
                if first_element_window <= idx_indices[target] <= last_element_window :
                    graph_samples[k] = [window,target] 
                    k+=1
    return graph_samples # it returns a dict with a list of indexes

def normalize(value,mean,std):
    return (value-mean)/std if std !=0 else Exception('std == 0')

def normalize_per_location(value, feature, location, int_name_normal_coef = int_name_normal_coef):
    return normalize(value, int_name_normal_coef[location]['mean'][feature], int_name_normal_coef[location]['std'][feature])

def train_test_split(samples, test_size):
    total_samples_list = list(samples.keys())
    test_ids = set(random.sample(total_samples_list, int(test_size * len(total_samples_list))))  
    train_ids = [k for k in total_samples_list if k not in test_ids]
    return train_ids, list(test_ids)

def create_mongodb_graphsample(samples, config, mode = 'train'):
    ## make connection to pure mongodb database and get the collection
    client = MongoClient("mongodb://localhost:27017/")
    db = client[config['db_name']] # meteo_paranal_test
    pure_collection = db[config['collection_pure_samples']]
    ####
    graph_samples = []
    print(f'Starting to build graph samples...({mode})')
    for j, id in enumerate(tqdm(samples.keys())):
        
        id_list_context = samples[id][0]
        id_list_target = samples[id][1]

        cursor = pure_collection.find({"idx": {"$in": id_list_context}}) # puntero con las direcciones 
        node_features =[]
        type_index = []
        spatial_index = []
        time = []
        for element in cursor:
            time.append( datetime.strptime(element['time'], '%Y-%m-%dT%H:%M:%S') )
            node_features.append(normalize_per_location(value = element['node_features'], 
                                                        feature = element['type_index'], 
                                                        location = element['spatial_index']
                                                        )
            )
            type_index.append(element['type_index'])
            spatial_index.append(element['spatial_index'])

        # normalizing time ...
        last_timestamp = time[-1]
        for i in range(len(time)):
            time[i] = (last_timestamp-time[i]).total_seconds() / config['time_norm']

        graph_sample = dict()
        graph_sample['time'] = time
        graph_sample['node_features'] = node_features
        graph_sample['type_index'] = type_index
        graph_sample['spatial_index'] = spatial_index
        graph_sample['key_padding_mask'] = (np.zeros_like(node_features) != 0).tolist()   
        graph_sample['kaboom'] = 'kaboom'

        #target
        target = pure_collection.find_one({"idx": id_list_target},{'_id':0,'idx':0})
        target_sample = dict()
        target_sample['time'] = [(last_timestamp - datetime.strptime(target['time'], 
                                                                     '%Y-%m-%dT%H:%M:%S')).total_seconds()/ config['time_norm']]
        target_sample['features'] = [normalize_per_location(value = target['node_features'], 
                                                            feature = target['type_index'], 
                                                            location = target['spatial_index'])]
        target_sample['type_index'] = [target['type_index']]
        target_sample['spatial_index'] = [target['spatial_index']]
        target_sample['dummy'] = None # checkear

        # adding target to sample
        graph_sample['target'] = target_sample
        graph_sample['id'] = j

        # append it all samples to a dict
        graph_samples.append(graph_sample)

    ## creating a collection with graphs samples 
    if mode == 'test':
        collection_graph_samples = db[config['collection_test']]
        print('Inserting samples in test collection...')
    else: 
        collection_graph_samples = db[config['collection_train']]
        print('Inserting samples in train collection...')

    if collection_graph_samples.count_documents({})>0: # if there is something in collection, drop it
        collection_graph_samples.drop()

    collection_graph_samples.insert_many(graph_samples)
    print(j+1,' Samples inserted!')

    client.close()

    return j

def create_train_test_db(samples, config, test_size):
    train_ids, test_ids = train_test_split(samples, test_size = test_size)
    print(f'{len(train_ids)} expeted to be inserted in train collection, and {len(test_ids)} in test collection.')
    len_train = create_mongodb_graphsample({key: samples[key] for key in train_ids}, config, mode = 'train')
    len_test = create_mongodb_graphsample({key: samples[key] for key in test_ids}, config, mode = 'test')
    return len_train, len_test

def create_samples():
    with open('config.yaml','r') as f:
        config = yaml.safe_load(f)   
    ids = get_sorted_idx_list(config)
    # ids = list(range(1000))

    samples = get_graph_sample_idx(context_len = config['context_len'], 
                                   stride = config['stride'], 
                                   idx_list = ids, 
                                   selection_size = config['remove']
                                   )
    len_train, len_test = create_train_test_db(samples, config, test_size = 0.3)
    config['len_train'] = len_train+1 # total samples, not last id
    config['len_test'] = len_test+1
    with open("config.yaml","w") as file:
        yaml.dump(config,file)

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

    # sample = dataloader[0]
    # assert isinstance(sample,ContinuousTimeGraphSample)
    # print(sample)

if __name__ == '__main__':
    # test()
    test_dataloader()
