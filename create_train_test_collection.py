import yaml
import random
import numpy as np
# import torch
# from torch.utils.data import Dataset, DataLoader
from pymongo import MongoClient
from datetime import datetime
from tqdm import trange, tqdm
import argparse
# from AGG.extended_typing import ContinuousTimeGraphSample

with open('utils/yaml/int_name_normal_coef.yaml','r') as f:
    int_name_normal_coef = yaml.safe_load(f)

def get_sorted_idx_list(config:dict)->list:
    """
    Here we connect to our mongodb database with all samples, and we create a list of sort indexes by datetime
    :param config: dictionary which has all the information to connect to mongodb database
    """
    client = MongoClient(config['host_port'])
    db = client[config['db_name']] 
    collection = db[config['collection_pure_samples']]
    ids = [elem['idx'] for elem in collection.find({}, {'idx': 1}).sort("time", 1)]
    client.close()
    return ids

def get_graph_sample_idx(context_len, stride, idx_list, selection_size) -> dict:
    """
    This function takes all the Ids which has each sample in our mongodb database, and with its parameters creates a list 
    of indexes of each ContinuousTimeGraphSample
    :param context_len: input block length
    :param stride: number of steps the block is moved before it is considered the next input to the AGG 
    :param idx_list: all the indexes of samples located in mongodb database
    :param selection_size: it is a % in how many samples we want to remove
    :return: dict
    """

    targets = set(random.sample(idx_list, int(selection_size * len(idx_list))))  # we select randomly the targets from idx_list
    print('Total targets: ',len(targets))
    train_nodes = [k for k in idx_list if k not in targets] # O(1) targets is save it as by hash table
    N = len(train_nodes)
    print('Total train nodes: ', N)
    windows = []
    idx_indices = {idx: i for i, idx in enumerate(idx_list)} # we create a map between indexes and lists of each samples, it's take O(1) doing this 
    k=0
    graph_samples = dict()
    print('Creating indexes of nodes...')
    for i in trange(0, N, stride):
        max_idx = min(i + context_len, N) 
        window = train_nodes[i:max_idx] 
        if len(window)==context_len: # we ask to the window to have exact lenght of the block
            windows.append(window) 
            first_element_window = idx_indices[window[0]]
            last_element_window = idx_indices[window[-1]]
            for target in targets :  # we iterate over each target in order to see if it is in the range of the context block
                if first_element_window <= idx_indices[target] <= last_element_window :
                    graph_samples[k] = [window,target] 
                    k+=1
    return graph_samples # it returns a dict with a list of indexes

def normalize(value,mean,std):
    return (value-mean)/std if std !=0 else Exception('std == 0')

def normalize_per_location(value, feature, location, int_name_normal_coef = int_name_normal_coef):
    """
    Function that normalize a value according to the location 
    """
    return normalize(value, int_name_normal_coef[location]['mean'][feature], int_name_normal_coef[location]['std'][feature])

def train_test_split(samples:dict, test_size:float):
    """
    This funciton takes the samples dictionary made it from get_graph_sample_idx() and returns its split of indexes according to train and test
    """
    total_samples_list = list(samples.keys())
    test_ids = set(random.sample(total_samples_list, int(test_size * len(total_samples_list))))  
    train_ids = [k for k in total_samples_list if k not in test_ids]
    return train_ids, list(test_ids) # lists of indexes according to train and test

def create_mongodb_graphsample(samples:dict, config:dict, int_name_normal_coef:dict, mode = 'train'):
    """
    This Function can create two collections in mongodb one with train samples and other with test samples, and returns the total samples located in that collection. 
    Those samples will be use in ContinuousTimeGraphSample class.
    The samples which takes are from train_test_split() function.
    """

    ## make connection to pure mongodb database and get the collection
    client = MongoClient(config['host_port'])
    db_name = config['db_name']
    db = client[db_name] 
    pure_collection = db[config['collection_pure_samples']]
    graph_samples = []
    print(f'Starting to build graph samples...({mode})')
    for j, id in enumerate(tqdm(samples)):
        
        id_list_context = samples[id][0]
        id_list_target = samples[id][1]

        context_cursor = pure_collection.find({"idx": {"$in": id_list_context}}) # puntero con las direcciones 
        node_features =[]
        type_index = []
        spatial_index = []
        time = []
        for element in context_cursor:
            time.append( datetime.strptime(element['time'], '%Y-%m-%dT%H:%M:%S') )
            node_features.append(normalize_per_location(value = element['node_features'], 
                                                        feature = element['type_index'], 
                                                        location = element['spatial_index'],
                                                        int_name_normal_coef = int_name_normal_coef
                                                        )
            )
            type_index.append(element['type_index'])
            spatial_index.append(element['spatial_index'])

        # normalizing time ...
        last_timestamp = time[-1] # I select the last datetime
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
                                                            location = target['spatial_index'],
                                                            int_name_normal_coef = int_name_normal_coef)]
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
        name_collection = config['collection_train']

        print('Inserting samples in test collection...')
    else: 
        collection_graph_samples = db[config['collection_train']]
        name_collection = config['collection_train']
        print('Inserting samples in train collection...')

    if collection_graph_samples.count_documents({})>0: # if there is something in collection, drop it
        collection_graph_samples.drop()

    collection_graph_samples.insert_many(graph_samples)
    print(j+1,f' Samples inserted in collection "{name_collection}" of database "{db_name}"')

    client.close()

    return j

def create_train_test_db(samples:dict, config:dict, int_name_normal_coef:dict, test_size:float):
    """
    Functions that creates a mongogodb collection for train and test samples.
    The datareader takes this samples.
    Returns the last sample id of train and test, i.e. if n is the last sample of train, and m for test,
    the total length of train is n+1 and for test m+1.
    """
    train_ids, test_ids = train_test_split(samples = samples, test_size = test_size)
    print(f'{len(train_ids)} samples expeted to be inserted in train collection, and {len(test_ids)} in test collection.')
    len_train = create_mongodb_graphsample(samples = {key: samples[key] for key in train_ids}, config = config, int_name_normal_coef = int_name_normal_coef, mode = 'train')
    len_test = create_mongodb_graphsample(samples = {key: samples[key] for key in test_ids}, config = config, int_name_normal_coef = int_name_normal_coef, mode = 'test')
    return len_train, len_test

def create_samples(type: str):
    with open('utils/yaml/int_name_normal_coef.yaml','r') as f:
        int_name_normal_coef = yaml.safe_load(f)
    with open('config.yaml','r') as f:
        config = yaml.safe_load(f)  

    if type == 'Test' :
        ids = list(range(1000))
    else: ids:list = get_sorted_idx_list(config)

    samples:dict = get_graph_sample_idx(context_len = config['context_len'], 
                                   stride = config['stride'], 
                                   idx_list = ids, 
                                   selection_size = config['remove']
                                   )
    len_train, len_test = create_train_test_db(samples, config, int_name_normal_coef, test_size = 0.3)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Testing or not graph sample collection')
    parser.add_argument('type', choices=['','Test'])
    args = parser.parse_args()
    if args.type == 'Test':
        create_samples(type = 'Test')
    else:
        create_samples(type = None)
