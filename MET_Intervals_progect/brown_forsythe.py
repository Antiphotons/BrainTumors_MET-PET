import pandas as pd
import numpy as np
from scipy.stats import levene


def variances(path):
    df = pd.read_csv(path, sep='\t')
    params = [df.columns[i].split('_')[0] for i in range(1, df.shape[1], 6)]  # derive parameters names
    resids = [df.columns[i].split('_')[1] for i in range(1, 7)][0:3]  # derive residuals names and filter first three
    var_df = pd.DataFrame(data=None, index=params, columns=resids)  # empty dataframe for variances

    for r in resids:
        for p in params:
            col = df[p + '_' + r]
            var_df[r][p] = (round(np.var(col), 3))
    return var_df


def brown_forsythe(path):
    df = pd.read_csv(path, sep='\t')
    new_columns = [df.columns[i] for i in range(1, len(df.columns)) if i % 6 in [1, 2, 3]]  # derive st-i columns names
    bf_df = pd.DataFrame(data=None, index=new_columns, columns=new_columns)  # empty df for brown-forsythe p-values

    for c1 in bf_df.columns:
        col1 = df[c1]
        for c2 in bf_df.columns:
            col2 = df[c2]
            stats, bf = levene(col1, col2, center='median')
            bf_df[c1][c2] = round(bf, 4)
    return bf_df


folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/csv/'
file1 = 'residuals.csv'
file2 = 'relative_residuals.csv'

res_var_df, res_bf_df = variances(folder + file1), brown_forsythe(folder + file1)
rel_res_var_df, rel_res_bf_df = variances(folder + file2), brown_forsythe(folder + file2)

res_var_df.to_csv('residuals_variances.csv', sep='\t')
rel_res_var_df.to_csv('rel_residuals_variances.csv', sep='\t')
res_bf_df.to_csv('residuals_bf.csv', sep='\t')
rel_res_bf_df.to_csv('rel_residuals_bf.csv', sep='\t')
