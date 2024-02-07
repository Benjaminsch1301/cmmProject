Pipeline Data Develop for GNN 

1. In order to download La silla and Paranal meteorological data, run:

        python download.py lasilla --start_year 1991 --end_year 2024
        python download.py paranal --start_year 1998 --end_year 2024

2. See folders "laSilla" and "paranal" where you can find notebooks with data analysis (missing data, count data, distributions, time series plot, etc.)

3. In order to get normal coeficients (mean and standard deviation), run:
        python get_normal_coef.py 
    And it will generate the next files with that information:
        normal_coef_lasilla.yaml
        normal_coef_paranal.yaml

4. Datareader for La Silla and Paranal is in datareader.py  