import pandas as pd
import numpy as np
from scipy.stats import levene


def brown_forsythe(array1, array2):
    stats, bf = levene(array1, array2, center='median')
    return bf


folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/csv/'
file = 'residuals.csv'

df = pd.read_csv(folder + file, sep='\t')
params = [df.columns[i].split('_')[0] for i in range(1, df.shape[1], 6)]  # derive parameters names
resids = [df.columns[i].split('_')[1] for i in range(1, 7)][0:3]  # derive residuals names and filter first three

var_df = pd.DataFrame(data=None, index=params, columns=resids)  # empty dataframe for variances
bf_df = pd.DataFrame(data=None, index=df.columns[1:], columns=df.columns[1:])  # empty df for brown-forsythe p-values

for r in resids:
    prev_col = df[params[0] + '_' + r]
    for p in params:
        col = df[p + '_' + r]
        var_df[r][p] = (round(np.var(col), 3))
        stats, bf = levene(col, prev_col, center='median')
        #print(round(bf, 4))
        prev_col = col


print(var_df)
print(bf_df)
