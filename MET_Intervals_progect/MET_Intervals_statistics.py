import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


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
    res_st1 = dataframe[columnst] - dataframe[column1]
    res_st2 = dataframe[columnst] - dataframe[column2]
    res_st3 = dataframe[columnst] - dataframe[column3]
    res_21 = dataframe[column2] - dataframe[column1]
    res_31 = dataframe[column3] - dataframe[column1]
    res_32 = dataframe[column3] - dataframe[column2]
    res_df = pd.DataFrame({
        parameter + '_st-1': res_st1,
        parameter + '_st-2': res_st2,
        parameter + '_st-3': res_st3,
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
    rel_res_st1 = (dataframe[columnst] - dataframe[column1]) / dataframe[columnst] * 100
    rel_res_st2 = (dataframe[columnst] - dataframe[column2]) / dataframe[columnst] * 100
    rel_res_st3 = (dataframe[columnst] - dataframe[column3]) / dataframe[columnst] * 100
    rel_res_21 = (dataframe[column2] - dataframe[column1]) / dataframe[column1] * 100
    rel_res_31 = (dataframe[column3] - dataframe[column1]) / dataframe[column1] * 100
    rel_res_32 = (dataframe[column3] - dataframe[column2]) / dataframe[column1] * 100
    rel_res_df = pd.DataFrame({
        parameter + '_st-1': rel_res_st1,
        parameter + '_st-2': rel_res_st2,
        parameter + '_st-3': rel_res_st3,
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
Int_dataframe = Int_dataframe[Int_dataframe.Case.notnull()].reset_index()
del Int_dataframe['index']

# creating an empty tables with residuals
res_dataframe, rel_res_dataframe = pd.DataFrame(), pd.DataFrame()

# creating an empty table with medians
parameters = ['SUVnorm', 'SUV1.3', 'SUV10', 'SUVmax', 'TBR1.3', 'TBR10', 'TBRmax', 'TMV1.3']
intervals = ['st', '1', '2', '3']
median_df = pd.DataFrame(
    {
        'st': ['', '', '', '', '', '', '', ''],
        '1': ['', '', '', '', '', '', '', ''],
        '2': ['', '', '', '', '', '', '', ''],
        '3': ['', '', '', '', '', '', '', ''],
        '2-1': ['', '', '', '', '', '', '', ''],
        '3-2': ['', '', '', '', '', '', '', '']
    },
    index=parameters,
)
median_df.index.name = 'Parameter'

# creating an unfilled table with medians of residuals
res_median_df = pd.DataFrame(
    {
        'st-1': ['', '', '', '', '', '', '', ''],
        'st-2': ['', '', '', '', '', '', '', ''],
        'st-3': ['', '', '', '', '', '', '', '']
    },
    index=parameters,
)
res_median_df.index.name = 'Parameter'

rel_res_median_df = res_median_df.copy(deep=True)  # unfilled table with medians of relative residuals

# filter the benign and malignant lesions
ben_int_df = Int_dataframe[Int_dataframe.Malignancy == 'Benign'].reset_index()
del ben_int_df['index']
mal_int_df = Int_dataframe[Int_dataframe.Malignancy == 'Malignant'].reset_index()
del mal_int_df['index']
ben_rel_res_df, mal_rel_res_df = rel_res_dataframe.copy(deep=True), rel_res_dataframe.copy(deep=True)  # empty df
ben_median_df, mal_median_df = median_df.copy(deep=True), median_df.copy(deep=True)  # unfilled dataframes of medians


for prmtr in parameters:
    # calculate the differences between intervals

    # join absolute residuals
    res_dataframe = np.round(pd.concat([res_dataframe, residuals(Int_dataframe, prmtr)], axis=1), 3)
    # join relative residuals
    rel_res_dataframe = np.round(pd.concat([rel_res_dataframe, rel_residuals(Int_dataframe, prmtr)], axis=1), 3)
    # repeat last step for benign and malignant lesions
    ben_rel_res_df = np.round(pd.concat([ben_rel_res_df, rel_residuals(ben_int_df, prmtr)], axis=1), 3)
    mal_rel_res_df = np.round(pd.concat([mal_rel_res_df, rel_residuals(mal_int_df, prmtr)], axis=1), 3)

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

    for rel_res in ['2-1', '3-2']:
        rr = prmtr + '_' + rel_res
        rel_res_med_quart = column_median(rel_res_dataframe, rr)  # calculate medians and quartiles of % residuals
        median_df[rel_res].loc[prmtr] = rel_res_med_quart  # fill out the median tables

        # repeat for benign and malignant lesions
        ben_rel_res_med_quart = column_median(ben_rel_res_df, rr)
        mal_rel_res_med_quart = column_median(mal_rel_res_df, rr)
        ben_median_df[rel_res].loc[prmtr] = ben_rel_res_med_quart
        mal_median_df[rel_res].loc[prmtr] = mal_rel_res_med_quart

    # calculate medians & quartiles of differences between 20 and 10 min intervals
    for res in ['st-1', 'st-2', 'st-3']:
        r = prmtr + '_' + res
        res_med_quart = column_median(res_dataframe, r)  # calculate medians and quartiles of residuals
        res_median_df[res].loc[prmtr] = res_med_quart  # fill out the res median tables

        # repeat for relative residuals
        rel_res_med_quart2 = column_median(rel_res_dataframe, r)
        rel_res_median_df[res].loc[prmtr] = rel_res_med_quart2


#res_dataframe.to_csv('residuals.csv', sep='\t')  # save absolute residuals to .csv
#rel_res_dataframe.to_csv('relative_residuals.csv', sep='\t')  # save relative (%) residuals to .csv
#median_df.to_csv('medians_and_quartiles.csv', sep='\t')  # save parameter medians & quartiles to .csv
#res_median_df.to_csv('res_medians_and_quartiles.csv', sep='\t')  # save residuals medians & quartiles to .csv
rel_res_median_df.to_csv('rel_res_medians_and_quartiles.csv', sep='\t')  # relative residuals medians & quartiles
#ben_median_df.to_csv('ben_medians_and_quartiles.csv', sep='\t')  # save benign medians & quartiles to .csv
#mal_median_df.to_csv('mal_medians_and_quartiles.csv', sep='\t')  # save malignant medians & quartiles to .csv
