import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Function for computation medians and quartiles of indexes
def column_median(dataframe, column):
    median = np.percentile(dataframe[column], 50)
    low_quartile = np.percentile(dataframe[column], 25)
    high_quartile = np.percentile(dataframe[column], 75)
    return str(median) + ' (' + str(low_quartile) + '–' + str(high_quartile) + ')'


# path to csv-file with data
folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/'
file = 'Intervals.csv'

# empty rows deletion
Int_dataframe = pd.read_csv(folder + file, sep='\t')
Int_dataframe = Int_dataframe[Int_dataframe.Case != ''].reset_index()
del Int_dataframe['Index']

# creation of table with medians
parameters = ['SUVnorm', 'SUV1.3', 'SUV10mm', 'SUVmax', 'TBR1.3', 'TBRmax', 'TBR10', 'TMV1.3']
intervals = ['st', '1', '2', '3']
median_df = pd.DataFrame({
    'st': [],
    '1': [],
    '2': [],
    '3': []
})
median_df.index = parameters
median_df.index.name = 'Parameter'

for prmtr in parameters:
    for intrv in intervals:
        p = prmtr + '-' + intrv
        med_quart = column_median(Int_dataframe, p)
        median_df[intrv].loc[prmtr] = med_quart
