import pandas as pd
import numpy as np
from scipy.stats import levene
from scipy.stats import median_abs_deviation
import statsmodels.stats.multitest as sm
import matplotlib.pyplot as plt
import seaborn as sns


# function for dataset loading and processing preparing
def df_load(path, option, res_type='standard'):
    df = pd.read_csv(path, sep='\t')
    params = [df.columns[i].split('_')[0] for i in range(1, df.shape[1], 6)]  # derive parameters names
    if res_type == 'standard':  # derive residuals names
        resids = [df.columns[i].split('_')[1] for i in range(1, 7)][0:3]  # filter first three
    elif res_type == 'reduced':
        resids = [df.columns[i].split('_')[1] for i in range(1, 7)][3:6]  # filter second three
    new_df = pd.DataFrame(data=None, index=params, columns=resids)  # empty dataframe for filling
    options = {'df': 0, 'params': 1, 'resids': 2, 'new_df': 3}
    opt = [df, params, resids, new_df]
    return opt[options.get(option)]


# function for computation of residual variances
def variances(path, dig):

    # dataframe loading
    df, params, resids, var_df = df_load(path, 'df'), df_load(path, 'params'), \
                                 df_load(path, 'resids'), df_load(path, 'new_df')
    # dataframe filling
    for r in resids:
        for p in params:
            col = df[p + '_' + r]
            var_df[r][p] = (round(np.var(col), dig))
    return var_df


# function for computation of residual median absolute deviations
def mad(path, dig):

    # dataframe loading
    df, params, resids, mad_df = df_load(path, 'df'), df_load(path, 'params'), \
                                 df_load(path, 'resids'), df_load(path, 'new_df')

    # dataframe filling
    for r in resids:
        for p in params:
            col = df[p + '_' + r]
            mad_df[r][p] = (round(median_abs_deviation(col), dig))
    return mad_df


# function for computation of Brown-Forsythe p-values (significance of variance difference)
def brown_forsythe(path, dig):

    # dataframe loading
    df, params, resids = df_load(path, 'df'), df_load(path, 'params'), df_load(path, 'resids')
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
def bootstrap(path, moment, iterations, dig, type):

    # dataframe loading
    df, params, resids, bs_df = df_load(path, 'df'), df_load(path, 'params'), \
                                 df_load(path, 'resids'), df_load(path, 'new_df')

    df = df[df['TMV1.3_3-st'] <= 100]

    # dataframe filling
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
                elif moment == 'loa':  # single limit of agreement
                    bs_moments.append(np.std(smpl) * 1.96)
                else:
                    print('please enter the allowable stat measure: mean, sd or loa')
                    break

            # histograms plotting for all parameters
            plt.hist(bs_moments)
            plt.savefig(p + '_' + r + '_' + moment + '_hist.png')
            plt.clf()

            # multiple hypothesis adjust
            adj_per = round(2.5 / (len(params) * len(resids)), 3)

            # dataframe with means and adjusted for p*r multiple hypotheses percentilles
            if type == 'txt':
                bs_df[r][p] = str(round(np.mean(bs_moments), dig)) + '(' + \
                          str(round(np.percentile(bs_moments, adj_per), dig)) + '–' +\
                          str(round(np.percentile(bs_moments, 100 - adj_per), dig)) + ')'
            elif type == 'num':
                bs_df[r][p] = [round(np.mean(bs_moments), dig),
                               round(np.percentile(bs_moments, adj_per), dig),
                               round(np.percentile(bs_moments, 100 - adj_per), dig)]
    return bs_df


# function for limits of agreement computation and text representation
def loas(mean_df, loa_df, dig=2):
    loas_df = pd.DataFrame(data=None, index=mean_df.index, columns=mean_df.columns)
    for i in mean_df.index:
        for c in mean_df.columns:
            loas_df[c][i] = str(round(mean_df[c][i][0] - loa_df[c][i][2], dig)) + '–' + \
                            str(round(mean_df[c][i][0] + loa_df[c][i][2], dig))
    return loas_df


# difference plotting
def boxplot(path):
    sns.set_theme(style="ticks")
    f, ax = plt.subplots(figsize=(8, 10))  # Initialize the figure

    # load dataframe
    df, params, resids = df_load(path, 'df'), df_load(path, 'params'), \
                                df_load(path, 'resids')
    param_list = [df.columns[i] for i in range(1, len(df.columns)) if i % 6 in [4, 5, 0]]

    # Plot with horizontal boxes
    sns.boxplot(data=df[param_list[:-3]], orient='h', dodge=False, whis=[2.5, 97.5], width=.6, palette="vlag")

    # Add in points to show each observation
    sns.stripplot(data=df[param_list[:-3]], orient='h', size=3, color=".3", linewidth=0)

    # Tweak the visual presentation
    plt.grid(True)
    # plt.xticks(range(-20, 50, 10), rotation=0)  # variant for relative SUVs and TBRs
    # plt.xticks(range(-100, 200, 50), rotation=0)  # variant for relative MTV
    ax.set(ylabel="")
    sns.despine(trim=True, left=True)
    plt.show()


folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/csv/'
file1 = 'residuals.csv'
file2 = 'relative_residuals.csv'

# classical nonparametric estimation of variability

res_mad_df, res_bf_df = mad(folder + file1, 3), brown_forsythe(folder + file1, 5)
rel_res_mad_df, rel_res_bf_df = mad(folder + file2, 1), brown_forsythe(folder + file2, 5)

# bootstrap estimation of bias and variability

res_ci95_df, res_loa_ci95_df = bootstrap(folder + file1, 'mean', 1000, 2, 'num'), \
                               bootstrap(folder + file1, 'loa', 1000, 2, 'num')
res_loas_df = loas(res_ci95_df, res_loa_ci95_df, 2)
rel_res_ci95_df, rel_res_loa_ci95_df = bootstrap(folder + file2, 'mean', 1000, 1, 'txt'), \
                                       bootstrap(folder + file2, 'loa', 1000, 1, 'num')
rel_res_loas_df = loas(rel_res_ci95_df, rel_res_loa_ci95_df, 1)

# Output block: tables and plots of descriptive statistics for differences (or residuals)
# and relative differences between three 10-min MET-PET intervals

res_mad_df.to_csv('residuals_mad.csv', sep='\t')  # Median average deviation (MAD)
rel_res_mad_df.to_csv('rel_residuals_mad.csv', sep='\t')  # MAD for relative residuals
res_bf_df.to_csv('residuals_bf.csv', sep='\t')  #  Brown-Forsythe p-values
rel_res_bf_df.to_csv('rel_residuals_bf.csv', sep='\t')  # B-F p for relative residuals
res_ci95_df.to_csv('residuals_ci95.csv', sep='\t')  # Mean and CI95 for residuals
rel_res_ci95_df.to_csv('rel_residuals_ci95.csv', sep='\t')  # Mean and CI95 for relative residuals
res_loas_df.to_csv('residuals_LoA.csv', sep='\t')  # limits of agreement (LoAs)
rel_res_loas_df.to_csv('rel_residuals_LoA.csv', sep='\t')  # LoAs for relative residuals
plot = boxplot(folder + file1)  # boxplot for all relative residuals
