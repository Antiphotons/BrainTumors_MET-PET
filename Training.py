#import os.path
import pandas as pd
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.stats import levene
#from statistics import mean, stdev
#import seaborn as sns

path_to_vois_folder = 'C:/PycharmProjects/Table_processer/Output/'
df = pd.read_csv(path_to_vois_folder + '001_Norma.csv', sep='\t')
copy_df = df.copy()
new_df = df.loc[:, ['Mean', 'VOI']]
copy_df['Halfmean'] = copy_df.Mean / 2

new_df['Dobblemean'] = new_df['Mean'] / copy_df['Halfmean']

print(new_df)
