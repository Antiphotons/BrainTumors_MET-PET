import os.path
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from scipy.stats import spearmanr, pearsonr
# from Difference_statistics import brown_forsythe


# Function for computation of medians and quartiles of indexes
def column_median(dataframe, column):
    median = round(np.percentile(dataframe[column], 50), 2)
    low_quartile = round(np.percentile(dataframe[column], 5), 2)
    high_quartile = round(np.percentile(dataframe[column], 95), 2)
    return str(median) + ' (' + str(low_quartile) + '–' + str(high_quartile) + ')'


# Function for computation of residuals
def residuals(dataframe, parameter):
    columnst = parameter + '-st'
    column1 = parameter + '-1'
    column2 = parameter + '-2'
    column3 = parameter + '-3'
    res_st1 = dataframe[column1] - dataframe[columnst]
    res_st2 = dataframe[column2] - dataframe[columnst]
    res_st3 = dataframe[column3] - dataframe[columnst]
    res_21 = dataframe[column2] - dataframe[column1]
    res_31 = dataframe[column3] - dataframe[column1]
    res_32 = dataframe[column3] - dataframe[column2]
    res_df = pd.DataFrame({
        parameter + '_1-st': res_st1,
        parameter + '_2-st': res_st2,
        parameter + '_3-st': res_st3,
        parameter + '_2-1': res_21,
        parameter + '_3-1': res_31,
        parameter + '_3-2': res_32
    })
    return res_df


# Function for computation of percent residuals
def rel_residuals(dataframe, parameter):
    columnst = parameter + '-st'
    column1 = parameter + '-1'
    column2 = parameter + '-2'
    column3 = parameter + '-3'
    rel_res_st1 = (dataframe[column1] - dataframe[columnst]) / dataframe[columnst] * 100
    rel_res_st2 = (dataframe[column2] - dataframe[columnst]) / dataframe[columnst] * 100
    rel_res_st3 = (dataframe[column3] - dataframe[columnst]) / dataframe[columnst] * 100
    rel_res_21 = (dataframe[column2] - dataframe[column1]) / dataframe[column1] * 100
    rel_res_31 = (dataframe[column3] - dataframe[column1]) / dataframe[column1] * 100
    rel_res_32 = (dataframe[column3] - dataframe[column2]) / dataframe[column2] * 100
    rel_res_df = pd.DataFrame({
        parameter + '_1-st': rel_res_st1,
        parameter + '_2-st': rel_res_st2,
        parameter + '_3-st': rel_res_st3,
        parameter + '_2-1': rel_res_21,
        parameter + '_3-1': rel_res_31,
        parameter + '_3-2': rel_res_32
    })
    return rel_res_df


# path to csv-file with data
folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/'
file = 'Intervals.csv'

# df load & empty rows deletion
Int_dataframe = pd.read_csv(folder + file, sep='\t', dtype={'Case': 'Int64'})
Int_dataframe = Int_dataframe[Int_dataframe.Case.notnull()].reset_index(drop=True)

# creating an empty tables with residuals
res_dataframe, rel_res_dataframe = pd.DataFrame(), pd.DataFrame()

# creating an empty table with medians
parameters = ['SUVnorm', 'SUV1.3', 'SUV10', 'SUVmax', 'TBR1.3', 'TBR10', 'TBRmax', 'TMV1.3']
intervals = ['st', '1', '2', '3']
resids = ['1-st', '2-st', '3-st', '2-1', '3-2', '3-1']
median_df = pd.DataFrame(
    {
        'st': ['', '', '', '', '', '', '', ''],
        '1': ['', '', '', '', '', '', '', ''],
        '2': ['', '', '', '', '', '', '', ''],
        '3': ['', '', '', '', '', '', '', ''],
        '2-1': ['', '', '', '', '', '', '', ''],
        '3-2': ['', '', '', '', '', '', '', ''],
        '3-1': ['', '', '', '', '', '', '', '']
    },
    index=parameters,
)
median_df.index.name = 'Parameter'

# creating an unfilled table with medians of residuals
res_median_df = pd.DataFrame(
    {
        '1-st': ['', '', '', '', '', '', '', ''],
        '2-st': ['', '', '', '', '', '', '', ''],
        '3-st': ['', '', '', '', '', '', '', '']
    },
    index=parameters,
)
res_median_df.index.name = 'Parameter'

rel_res_median_df = res_median_df.copy(deep=True)  # unfilled table with medians of relative residuals

# filter the benign and malignant lesions
ben_int_df = Int_dataframe[Int_dataframe.Malignancy == 'Benign'].reset_index(drop=True)
mal_int_df = Int_dataframe[Int_dataframe.Malignancy == 'Malignant'].reset_index(drop=True)
ben_rel_res_df, mal_rel_res_df = rel_res_dataframe.copy(deep=True), rel_res_dataframe.copy(deep=True)  # empty df
ben_median_df, mal_median_df = median_df.copy(deep=True), median_df.copy(deep=True)  # unfilled dataframes of medians


for prmtr in parameters:
    # calculate the differences between intervals

    # join residuals
    res_dataframe = np.round(pd.concat([res_dataframe, residuals(Int_dataframe, prmtr)], axis=1), 3)
    # join relative (percent) residuals
    rel_res_dataframe = np.round(pd.concat([rel_res_dataframe, rel_residuals(Int_dataframe, prmtr)], axis=1), 3)
    # repeat last step for benign and malignant lesions
    ben_rel_res_df = np.round(pd.concat([ben_rel_res_df, rel_residuals(ben_int_df, prmtr)], axis=1), 3)
    mal_rel_res_df = np.round(pd.concat([mal_rel_res_df, rel_residuals(mal_int_df, prmtr)], axis=1), 3)
    # generate dataframes with absolute values of residuals
    abs_res_dataframe, abs_rel_res_dataframe = abs(res_dataframe), abs(rel_res_dataframe)

    # calculate medians & quartiles and join them to dataframe
    for intrv in intervals:
        p = prmtr + '-' + intrv
        med_quart = column_median(Int_dataframe, p)  # calculate medians and quartiles of parameter on interval
        median_df[intrv].loc[prmtr] = med_quart  # fill out the median tables

        # repeat for benign and malignant lesions
        ben_med_quart = column_median(ben_int_df, p)
        ben_median_df[intrv].loc[prmtr] = ben_med_quart
        mal_med_quart = column_median(mal_int_df, p)
        mal_median_df[intrv].loc[prmtr] = mal_med_quart

    for rel_res in ['2-1', '3-2', '3-1']:
        rr = prmtr + '_' + rel_res
        rel_res_med_quart = column_median(rel_res_dataframe, rr)  # calculate medians and quartiles of % residuals
        median_df[rel_res].loc[prmtr] = rel_res_med_quart  # fill out the median tables

        # repeat for benign and malignant lesions
        ben_rel_res_med_quart = column_median(ben_rel_res_df, rr)
        mal_rel_res_med_quart = column_median(mal_rel_res_df, rr)
        ben_median_df[rel_res].loc[prmtr] = ben_rel_res_med_quart
        mal_median_df[rel_res].loc[prmtr] = mal_rel_res_med_quart

    # calculate medians & quartiles of differences between 20 and 10 min intervals
    for res in ['1-st', '2-st', '3-st']:
        r = prmtr + '_' + res
        res_med_quart = column_median(res_dataframe, r)  # calculate medians and quartiles of residuals
        res_median_df[res].loc[prmtr] = res_med_quart  # fill out the res median tables

        # repeat for relative residuals
        rel_res_med_quart2 = column_median(rel_res_dataframe, r)
        rel_res_median_df[res].loc[prmtr] = rel_res_med_quart2


# res_dataframe.to_csv('residuals.csv', sep='\t')  # save absolute residuals to .csv
# rel_res_dataframe.to_csv('relative_residuals.csv', sep='\t')  # save relative (%) residuals to .csv
# abs_res_dataframe.to_csv('abs_residuals.csv', sep='\t')  # save absolute residuals to .csv
# abs_rel_res_dataframe.to_csv('abs_relative_residuals.csv', sep='\t')  # save absolute % residuals to .csv

# median_df.to_csv('medians_and_quartiles.csv', sep='\t')  # save parameter medians & quartiles to .csv
# res_median_df.to_csv('res_medians_and_quartiles.csv', sep='\t')  # save residuals medians & quartiles to .csv
# rel_res_median_df.to_csv('rel_res_medians_and_quartiles.csv', sep='\t')  # relative residuals medians & quartiles
# ben_median_df.to_csv('ben_medians_and_quartiles.csv', sep='\t')  # save benign medians & quartiles to .csv
# mal_median_df.to_csv('mal_medians_and_quartiles.csv', sep='\t')  # save malignant medians & quartiles to .csv


# correlations between uptake values and differences of these values on distinct intervals

val_res_df = pd.concat([Int_dataframe, res_dataframe], axis=1)  # join df for residuals
val_rel_res_df = pd.concat([Int_dataframe, rel_res_dataframe], axis=1)  # join df for % residuals
abs_res_df, abs_rel_res_df = abs(res_dataframe), abs(rel_res_dataframe)  # absolute residuals and % residuals df
val_abs_res_df = pd.concat([Int_dataframe, abs_res_df], axis=1)  # join df for abs residuals
val_abs_rel_res_df = pd.concat([Int_dataframe, abs_rel_res_df], axis=1)  # join df for abs % residuals

corr_df = pd.DataFrame(columns=resids, index=[p + '-' + i for p in parameters for i in intervals])
spearman, rel_spearman, abs_spearman, abs_rel_spearman = corr_df.copy(), corr_df.copy(), corr_df.copy(), corr_df.copy()
pearson, rel_pearson, abs_pearson, abs_rel_pearson = corr_df.copy(), corr_df.copy(), corr_df.copy(), corr_df.copy()

for p in parameters:
    for i in intervals:
        if i == 'st':
            for r in resids[:3]:

                # non-parametric correlations between residuals (abs, % and abs % residuals) and initial values

                spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).pvalue, 2))
                rel_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).pvalue, 2))
                abs_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).pvalue, 2))
                abs_rel_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).pvalue, 2))

                # parametric correlations (linear pearson)

                pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).pvalue, 2))
                rel_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).pvalue, 2))
                abs_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).pvalue, 2))
                abs_rel_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).pvalue, 2))

        elif i == '1':
            for r in ['2-1', '3-1']:
                spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).pvalue, 2))
                rel_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).pvalue, 2))
                abs_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).pvalue, 2))
                abs_rel_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).pvalue, 2))

                # parametric correlations (linear pearson)

                pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).pvalue, 2))
                rel_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).pvalue, 2))
                abs_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).pvalue, 2))
                abs_rel_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).pvalue, 2))

        elif i == '2':
            for r in ['3-2']:
                spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).pvalue, 2))
                rel_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).pvalue, 2))
                abs_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).pvalue, 2))
                abs_rel_spearman.loc[p + '-' + i, r] = \
                    (round(spearmanr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).correlation, 2),
                     round(spearmanr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).pvalue, 2))

                # parametric correlations (linear pearson)

                pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_res_df[p + '-' + i], val_res_df[p + '_' + r]).pvalue, 2))
                rel_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_rel_res_df[p + '-' + i], val_rel_res_df[p + '_' + r]).pvalue, 2))
                abs_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_abs_res_df[p + '-' + i], val_abs_res_df[p + '_' + r]).pvalue, 2))
                abs_rel_pearson.loc[p + '-' + i, r] = \
                    (round(pearsonr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).statistic, 2),
                     round(pearsonr(val_abs_rel_res_df[p + '-' + i], val_abs_rel_res_df[p + '_' + r]).pvalue, 2))

# spearman.to_csv('spearman_res.csv', sep='\t')
# rel_spearman.to_csv('spearman_rel_res.csv', sep='\t')
# abs_spearman.to_csv('spearman_abs_res.csv', sep='\t')
# abs_rel_spearman.to_csv('spearman_abs_rel_res.csv', sep='\t')

abs_spearman_st, abs_rel_spearman_st = abs_spearman.iloc[::4, :3], abs_rel_spearman.iloc[::4, :3]
spearman_st = pd.concat([abs_spearman_st, abs_rel_spearman_st], axis=0)
# spearman_st.to_csv('spearman_st.csv', sep='\t')

# pearson.to_csv('pearson_res.csv', sep='\t')
# rel_pearson.to_csv('pearson_rel_res.csv', sep='\t')
# abs_pearson.to_csv('pearson_abs_res.csv', sep='\t')
# abs_rel_pearson.to_csv('pearson_abs_rel_res.csv', sep='\t')

# val_res_dataframe.to_csv('intervals-residuals.csv', sep='\t')
# val_rel_res_dataframe.to_csv('intervals-rel_residuals.csv', sep='\t')
