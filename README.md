Pipeline Data Develop for GNN 

1. In order to download from La silla, Paranal and APEX meteorological data, run:

        python download.py lasilla --start_year 1993 --end_year 2024
        python download.py paranal --start_year 1998 --end_year 2024
        python download.py apex --start_year 2006 --end_year 2024

2. See folder "notebooks" where you can find .ipynb with data analysis (missing data, count data, distributions, time series plot, etc.)

3. In order to get normal coeficients (mean and standard deviation) for all datasets (Paranal, La Silla and APEX),  run:

        python get_normal_coef.py  all

    And it will generate the next files with that information:
    
        normal_coef_lasilla.yaml
        normal_coef_paranal.yaml
        normal_coef_apex.yaml

4. Datareader for La Silla, Paranal and APEX is in datareader.py  