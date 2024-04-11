# Pipeline Data Develop for GNN 

1. In order to download each dataset of La silla, Paranal and APEX meteorological data, run:

        python download.py lasilla --start_year 1993 --end_year 2024
        python download.py paranal --start_year 1998 --end_year 2024
        python download.py apex --start_year 2006 --end_year 2024

2. See folder "notebooks" where you can find .ipynb with data analysis (missing data, count data, distributions, time series plot, etc.)

3. In order to get normal coeficients (mean and standard deviation) for all datasets (Paranal, La Silla and APEX), it is need to be downloaded in separate collections each dataset, if you have that, run:

        python get_normal_coef.py  all

    And it will generate the next files with that information:
    
        normal_coef_lasilla.yaml
        normal_coef_paranal.yaml
        normal_coef_apex.yaml
        
4. To download each sample (which later we process it to use it in datareader) run **utils/download_as_sample.py**, with its configuration **utils/yaml/config_download**, where you can select start and end year to download, its location in mongodb (database and collection), and other information useful to download. 

5. Once all the samples are downloaded according to 4., we need to build each ContinuousTimeGraphSample according to all dataset, for that look up and just run **create_train_test_collection.py**, this code will create a train and test collection. Also in **datareader.py** you can find the datareader with ContinuousTimeGraphSample. All the parameters to build ContinuousTimeGraphSample are located in **config.yaml**, these are sparcity, stride and context lenght, and other corresponding to save in a mongodb database.

6. An example of what **create_train_test_collection.py** do is located in [example.ipynb](example.ipynb) . Also there is an example of how indexes are generated located in [testing_indexes.ipynb](testing_indexes.ipynb)