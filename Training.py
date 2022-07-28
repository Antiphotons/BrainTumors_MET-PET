import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Function for computation of medians and quartiles of indexes
def column_median(dataframe, column):
    median = np.percentile(dataframe[column], 50)
    low_quartile = np.percentile(dataframe[column], 25)
    high_quartile = np.percentile(dataframe[column], 75)
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

print(Int_dataframe)
