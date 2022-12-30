import pandas as pd
import numpy as np
from scipy.stats import levene
from scipy.stats import median_abs_deviation
import statsmodels.stats.multitest as sm
import matplotlib.pyplot as plt


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


# function for computation of Brown-Forsythe p-values (significance of variance difference)
def brown_forsythe(path, dig):
    df = pd.read_csv(path, sep='\t')
    params = [df.columns[i].split('_')[0] for i in range(1, df.shape[1], 6)]  # derive parameters names
    resids = [df.columns[i].split('_')[1] for i in range(1, 7)][0:3]  # derive residuals names and filter first three
    new_columns = [df.columns[i] for i in range(1, len(df.columns)) if i % 6 in [1, 2, 3]]  # derive st-i columns names
    bf_df = pd.DataFrame(data=None, index=new_columns, columns=new_columns)  # empty df for Brown-Forsythe p-values

    # Brown-Forsythe p-value computation
    for i1 in range(len(params)):
        for i2 in range(len(resids)):
            c1 = params[i1] + '_' + resids[i2]
            col1 = df[c1]
            for j2 in range(i2 + 1, len(resids)):
                c2 = params[i1] + '_' + resids[j2]
                col2 = df[c2]
                stats, bf = levene(col1, col2, center='median')
                bf_df[c1][c2] = round(bf, dig)
            for j1 in range(i1 + 1, len(params)):
                c2 = params[j1] + '_' + resids[i2]
                col2 = df[c2]
                stats, bf = levene(col1, col2, center='median')
                bf_df[c1][c2] = round(bf, dig)

    # multiple comparison correction for Brown-Forsythe p-values
    mc_df = pd.DataFrame(data=None, index=None, columns=['Param_pair', 'p_value'])
    for c1 in bf_df.columns:
        for c2 in bf_df.columns:
            if pd.notna(bf_df[c1][c2]):
                par_pair = c1 + '_-_' + c2
                p_val = bf_df[c1][c2]
                mc_df.loc[len(mc_df.index)] = [par_pair, p_val]

    holm = sm.multipletests(mc_df.p_value.tolist(), alpha=0.05, method='holm', is_sorted=False)
    mc_df['FWER'] = [round(holm[1][i], 4) for i in range(len(holm[1]))]
    mc_df_restr = mc_df[mc_df.FWER <= 0.05]
    return mc_df_restr


# function for computation of confidence intervals with bootstrap method
def bootstrap(path, moment, iterations, dig):
    df = pd.read_csv(path, sep='\t')
    params = [df.columns[i].split('_')[0] for i in range(1, df.shape[1], 6)]  # derive parameters names
    resids = [df.columns[i].split('_')[1] for i in range(1, 7)][0:3]  # derive residuals names and filter first three
    bs_df = pd.DataFrame(data=None, index=params, columns=resids)  # empty dataframe for variances

    for p in params:
        for r in resids:
            col = df[p + '_' + r]
            bs_moments = []
            for _ in range(iterations):
                smpl = np.random.choice(col, size=len(col), replace=True)
                if moment == 'mean':
                    bs_moments.append(np.mean(smpl))
                elif moment == 'sd':
                    bs_moments.append(np.std(smpl))
                else:
                    print('please enter the allowable stat measure: mean or sd')
                    break

            # histograms plotting for all parameters
            plt.hist(bs_moments)
            plt.savefig(p + '_' + r + '_' + moment + '_hist.png')
            plt.clf()

            # dataframe with means and adjusted for 24 multiple hypotheses percentilles
            bs_df[r][p] = str(round(np.mean(bs_moments), dig)) + '(CI95 ' + \
                          str(round(np.percentile(bs_moments, 0.104), dig)) + '–' +\
                          str(round(np.percentile(bs_moments, 99.896), dig)) + ')'
    return bs_df


folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/csv/'
file1 = 'residuals.csv'
file2 = 'relative_residuals.csv'

# classical nonparametric estimation of variability
# res_mad_df, res_bf_df = mad(folder + file1, 3), brown_forsythe(folder + file1, 5)
# rel_res_mad_df, rel_res_bf_df = mad(folder + file2, 1), brown_forsythe(folder + file2, 5)

# bootstrap estimation of bias and variability
res_ci95_df, res_sd_ci95_df = bootstrap(folder + file1, 'mean', 5000, 2), bootstrap(folder + file1, 'sd', 5000, 2)
rel_res_ci95_df, rel_res_sd_ci95_df = bootstrap(folder + file2, 'mean', 5000, 1), \
                                      bootstrap(folder + file2, 'sd', 5000, 1)

# output block
# res_mad_df.to_csv('residuals_mad.csv', sep='\t')
# rel_res_mad_df.to_csv('rel_residuals_mad.csv', sep='\t')
# res_bf_df.to_csv('residuals_bf.csv', sep='\t')
# rel_res_bf_df.to_csv('rel_residuals_bf.csv', sep='\t')
res_ci95_df.to_csv('residuals_ci95.csv', sep='\t')
rel_res_ci95_df.to_csv('rel_residuals_ci95.csv', sep='\t')
res_sd_ci95_df.to_csv('residuals_sd.csv', sep='\t')
rel_res_sd_ci95_df.to_csv('rel_residuals_sd.csv', sep='\t')
