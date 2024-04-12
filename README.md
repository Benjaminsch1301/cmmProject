# Pipeline Data Develop for GNN 

1. In order to download each dataset of La silla, Paranal and APEX meteorological data for Analysis or get normal coefficents, run:

        python download.py lasilla --start_year 1993 --end_year 2024
        python download.py paranal --start_year 1998 --end_year 2024
        python download.py apex --start_year 2006 --end_year 2024

2. See folder "notebooks" where you can find .ipynb with data analysis (missing data, count data, distributions, time series plot, etc.) according to each dataset.

3. In order to download the dataset as a node of graph sample there are two ways, considering all the dataset or just a part as test, for that run, respectively:

        python download_as_sample.py All
        python download_as_sample.py Test

    Also it is important to set the location where we locate each sample, for that go to [utils/yaml/config_download.yaml](utils/yaml/config_download.yaml), here you will see database and collection name in mongodb, start and end year of all three datasets.

    The samples of this collection are useful later to build datareader, because each sample contains information about its value, location, feature and time, so this is almost ready to be a node in graph sample. The sample looks like this one:

        {'idx': 0, 'time': '2007-01-01T00:00:02', 'node_features': 15.32, 'type_index': 0, 'spatial_index': 0}

4. In order to get normal coeficients (mean and standard deviation) for all datasets (Paranal, La Silla and APEX), it is need to be downloaded in separate collections each dataset, if you have that, run:

        python get_normal_coef.py  all

    And it will generate the next files with that information:
    
        normal_coef_lasilla.yaml
        normal_coef_paranal.yaml
        normal_coef_apex.yaml

    But the normal coefficients are already calculated according to all three dataset historically, so **it is not necessary to do this step**. The coefficients are located in: [utils/yaml/int_name_normal_coef.yaml](utils/yaml/int_name_normal_coef.yaml)

5. Once all the samples are downloaded according to 3., we need to build each ContinuousTimeGraphSample, but first it is need to be set all the parameters which are related to mongodb location and others to construct each graph sample. For that go to [config.yaml](config.yaml) and set:

 - host_port: Mongo db host and port
 - db_name: database name where it is located each sample downloaded in 3.
 - collection_pure_samples: collection name where it is located each sample downloaded in 3.
 - collection_test: collection name where the test graph samples will be located
 - collection_train: collection name where the train graph samples will be located
 - remove: the percentage to remove
 - stride: the number of steps the block is moved before it is considered the next input to the AGG 
 - context_len: length of input block
 - N_block_insert: number of blocks of train samples to be inserted in collection (useful to save memory)

    Once all the parameters are set in [config.yaml](config.yaml), it is time to create the graph sample collection for train and test, for that run respectively:

        python create_train_test_collection.py

    or 

        python create_train_test_collection.py Test

    Additionally there is a code to insert samples by blocks in collections (train and test): [create_train_test_collection_block.py](create_train_test_collection_block.py). 

6. With the idea to sample from the train collection, there is a generic datareader located in [datareader.py](datareader.py). It is **important** to note that the length of the train and test collection is located in [config.yaml](config.yaml) in order to use it in datareader len method. Those "private" parameters are **len_test** and **len_test**, which it is recommended not be change them. 

7. Finally, An example of what **create_train_test_collection.py** do is located in [example.ipynb](example.ipynb) . Also there is an example of how indexes are generated located in [testing_indexes.ipynb](testing_indexes.ipynb).