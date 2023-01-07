#import os.path
import pandas as pd
from math import inf
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.stats import levene
#from statistics import mean, stdev
#import seaborn as sns

path_to_vois_folder = 'C:/PycharmProjects/Table_processer/Output/'
df = pd.read_csv(path_to_vois_folder + '020_Norma.csv', sep='\t')
del df['Unnamed: 0']
old_ind = df.Series[df.Series.str.contains('Dynamic') == False].index.tolist()
for i in range(len(old_ind)):
    df.rename(index={old_ind[i]: len(df.Series)+i}, inplace=True)
df.sort_index(ascending=True, inplace=True)
df = df.reset_index(drop=True)

print(df)
