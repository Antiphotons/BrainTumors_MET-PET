import pandas as pd
import numpy as np
from scipy.stats import levene


def brown_forsythe(dataframe, column):
    stats, bf = levene(dataframe[column], dataframe[column], center='median')
    return bf


folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/csv/'
file = 'residuals.csv'

df = pd.read_csv(folder + file, sep='\t')
params = [df.columns[i].split('_')[0] for i in range(1, df.shape[1], 6)]
resids = [df.columns[i].split('_')[1] for i in range(1, 7)]

var_df = pd.DataFrame(data=None, index=params, columns=resids)

for i in range(1, df.shape[1]):
    col = df.columns[i]
    variance = round(np.var(df[col]), 3)
    #print(variance)
