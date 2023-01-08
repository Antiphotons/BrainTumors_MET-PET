#import os.path
import pandas as pd
from math import inf
#import matplotlib.pyplot as plt
import numpy as np
#from scipy.stats import levene
#from statistics import mean, stdev
#import seaborn as sns

path_to_vois_folder = 'C:/PycharmProjects/Table_processer/Output/'
df = pd.read_csv(path_to_vois_folder + '020_Norma.csv', sep='\t')
del df['Unnamed: 0']
y_df = df.Mean
average = [np.percentile(y_df.loc[i], 50) for i in range(len(df.Mean))]  # median
# low_limit = [np.percentile(y_df.loc[i], 2.5) for i in range(len(tac_df.Time))]  # 1 quartile
# high_limit = [np.percentile(y_df.loc[i], 97.5) for i in range(len(tac_df.Time))]  # 3 quartile

print(average)
