#import os.path
import pandas as pd
from math import inf
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.stats import levene
#from statistics import mean, stdev
#import seaborn as sns

path_to_vois_folder = 'C:/PycharmProjects/Table_processer/Output/'
m = 'dich'
df = pd.read_csv(path_to_vois_folder + '020_Norma.csv', sep='\t')
del df['Unnamed: 0']
curve = pd.DataFrame()
curve['Mean'] = df.Mean[1:]
curve.reset_index()
curve['Time'] = df.index[1:] * 10
curve.loc[25, ['Mean']] = 1.37
m = max(curve['Mean'])
t_m = curve.Time[curve.Mean[curve.Mean == m].index[0]]

print(curve)
print()
print(t_m)
