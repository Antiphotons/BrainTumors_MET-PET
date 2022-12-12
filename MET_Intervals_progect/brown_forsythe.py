import pandas as pd
import numpy as np
from scipy.stats import levene
from scipy.stats import median_abs_deviation


# function for computation of residual variances
def variances(path, dig):
    df = pd.read_csv(path, sep='\t')
    params = [df.columns[i].split('_')[0] for i in range(1, df.shape[1], 6)]  # derive parameters names
    resids = [df.columns[i].split('_')[1] for i in range(1, 7)][0:3]  # derive residuals names and filter first three
    var_df = pd.DataFrame(data=None, index=params, columns=resids)  # empty dataframe for variances

    for r in resids:
        for p in params:
            col = df[p + '_' + r]
            var_df[r][p] = (round(np.var(col), dig))
    return var_df


# function for computation of residual median absolute deviations
def mad(path, dig):
    df = pd.read_csv(path, sep='\t')
    params = [df.columns[i].split('_')[0] for i in range(1, df.shape[1], 6)]  # derive parameters names
    resids = [df.columns[i].split('_')[1] for i in range(1, 7)][0:3]  # derive residuals names and filter first three
    mad_df = pd.DataFrame(data=None, index=params, columns=resids)  # empty dataframe for variances

    for r in resids:
        for p in params:
            col = df[p + '_' + r]
            mad_df[r][p] = (round(median_abs_deviation(col), dig))
    return mad_df


def brown_forsythe(path, dig):
    df = pd.read_csv(path, sep='\t')
    new_columns = [df.columns[i] for i in range(1, len(df.columns)) if i % 6 in [1, 2, 3]]  # derive st-i columns names
    bf_df = pd.DataFrame(data=None, index=new_columns, columns=new_columns)  # empty df for brown-forsythe p-values

    for c1 in bf_df.columns:
        col1 = df[c1]
        for c2 in bf_df.columns:
            col2 = df[c2]
            stats, bf = levene(col1, col2, center='median')
            bf_df[c1][c2] = round(bf, dig)
    return bf_df


folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/csv/'
file1 = 'residuals.csv'
file2 = 'relative_residuals.csv'

res_mad_df, res_bf_df = mad(folder + file1, 3), brown_forsythe(folder + file1, 5)
rel_res_mad_df, rel_res_bf_df = mad(folder + file2, 0), brown_forsythe(folder + file2, 5)

res_mad_df.to_csv('residuals_mad.csv', sep='\t')
rel_res_mad_df.to_csv('rel_residuals_mad.csv', sep='\t')
res_bf_df.to_csv('residuals_bf.csv', sep='\t')
rel_res_bf_df.to_csv('rel_residuals_bf.csv', sep='\t')
