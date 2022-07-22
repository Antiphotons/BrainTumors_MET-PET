import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/'
file = 'Intervals.csv'
Int_dataframe = pd.read_csv(folder + file, sep='\t')
Int_dataframe = Int_dataframe[Int_dataframe.Case != ''].reset_index()
del Int_dataframe['Index']
for prmtr in ['TBR1.3', 'TBRmax', 'TBR10', 'TMV1.3']:
    for intrv in ['st', '1', '2', '3']:
        p = prmtr + '-' + intrv
