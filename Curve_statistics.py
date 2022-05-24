import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# function to generate median & percentile curves from TACs
def curve_percentiles(tac_df):
    y_df = tac_df.drop(columns='Times')
    median = [np.percentile(y_df.loc[i], 50) for i in range(len(tac_df.Times))]
    low_percentile = [np.percentile(y_df.loc[i], 5) for i in range(len(tac_df.Times))]
    high_percentile = [np.percentile(y_df.loc[i], 95) for i in range(len(tac_df.Times))]
    tac_df['Median'], tac_df['Low_percentile'], tac_df['High_percentile'] = median, \
                                                                            low_percentile, high_percentile
    return tac_df


# function for load & transform VOI file to curve dataframe
def curve_loader(folder_path, file_name, measure_type):
    path = folder_path
    file = file_name  # input from user before function starts
    voi_dataframe = pd.read_csv(path + file, sep='\t')  # previous created VOI .csv
    # only dynamic data preserved
    voi_dataframe = voi_dataframe[voi_dataframe['Series'].str.contains('Dynamic')].reset_index()
    # detect type of curve (25 or 70 frames)
    if len(voi_dataframe.VOI) == 35:
        times = pd.Series([0, 5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 70, 80,
                           90, 100, 110, 120, 150, 180, 210, 240, 270, 300, 360, 420,
                           480, 540, 600, 900, 1200, 1500, 1800, 2100])
    elif len(voi_dataframe.VOI) < 26:
        times = pd.Series([0, 30, 60, 90, 120, 150, 180, 210, 240, 270, 300, 360, 420,
                           480, 540, 600, 780, 960, 1140, 1320, 1500, 1680, 1860, 2040, 2220])
    elif 25 < len(voi_dataframe.VOI) < 71:
        times = pd.Series([0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210,
                           225, 240, 255, 270, 285, 300, 315, 330, 345, 360, 375, 390, 405, 420,
                           435, 450, 465, 480, 495, 510, 525, 540, 555, 570, 585, 600, 630, 660,
                           690, 720, 750, 780, 810, 840, 870, 900, 930, 960, 990, 1020, 1050, 1080,
                           1110, 1140, 1170, 1200, 1320, 1440, 1560, 1680, 1800, 1920, 2040, 2160, 2280])
    else:
        print('error: check dynamic curve length')
    tac_dataframe = pd.DataFrame({
        measure_type: voi_dataframe[measure_type],  # type of activity value (mean, max, or peak)
        'Time': times  # time points
    })  # finalisation of curve dataframe
    return tac_dataframe


# function for reorganise 70-frame TAC to 30-frame TAC
def tac_smoother(tac_df, measure_type):
    if len(tac_df.Time) > 36:

        # 15-sec-frame to 30-sec-frame
        for i in range(0, 10):
            tac_df.loc[i, measure_type] = sum(tac_df[measure_type].loc[i:i + 1]) / 2
            tac_df.drop(tac_df.index[i + 1], inplace=True)
            tac_df = tac_df.reset_index()
            del tac_df['index']

        # 15-sec-frame to 60-sec-frame
        for i in range(10, 15):
            tac_df.loc[i, measure_type] = sum(tac_df[measure_type].loc[i:i + 3]) / 4
            tac_df.drop(tac_df.index[i + 3], inplace=True)
            tac_df.drop(tac_df.index[i + 2], inplace=True)
            tac_df.drop(tac_df.index[i + 1], inplace=True)
            tac_df = tac_df.reset_index()
            del tac_df['index']

        # 30-sec-frame to 120-sec-frame
        for i in range(15, 20):
            tac_df.loc[i, measure_type] = sum(tac_df[measure_type].loc[i:i + 3]) / 4
            tac_df.drop(tac_df.index[i + 3], inplace=True)
            tac_df.drop(tac_df.index[i + 2], inplace=True)
            tac_df.drop(tac_df.index[i + 1], inplace=True)
            tac_df = tac_df.reset_index()
            del tac_df['index']
    return tac_df


# function for reorganise 30-frame TAC to 25-frame TAC
def tac_transformer(tac_df, measure_type):
    if len(tac_df.Time) == 30:

        # 120-sec-frames to 180-sec-frames
        nw_tac_df = pd.DataFrame(columns=['Time', measure_type])
        for i in range(0, 15):
            nw_tac_df.loc[i] = tac_df.loc[i]
        cnt = 0
        for i in range(15, 30, 3):
            nw_tac_df.loc[i - cnt, measure_type] = sum(tac_df[measure_type].loc[i:i + 1]) / 2
            nw_tac_df.loc[i - cnt, 'Time'] = tac_df[i, 'Time']
            nw_tac_df.loc[i + 1 - cnt, measure_type] = sum(tac_df[measure_type].loc[i + 1:i + 2]) / 2
            nw_tac_df.loc[i + 1 - cnt, 'Time'] = tac_df[i, 'Time'] + 180
            cnt += 1
        nw_tac_df = nw_tac_df.reset_index()
        del nw_tac_df['index']
    return nw_tac_df


# function for generate dataframe consist of TACs of specific histotype, measure and roi
def filtered_tac_gen(folder_path, lesion_dataframe, histotype, roi, measure_type):
    filtr_lesion_df = lesion_dataframe[lesion_dataframe.Histo == histotype]

    for i in range(len(filtr_lesion_df.Les)):
        filename = str(filtr_lesion_df.Les[i]) + '_' + roi + '.csv'
        if os.path.exists(folder_path + filename):  # checking if a ROI file exists
            tac = curve_loader(folder_path, filename, measure_type)
            tac = tac_smoother(tac, measure_type)  # transform 70-frame-TACs
            tac = tac_transformer(tac, measure_type) # transform 30-frame-TACs to 25-frame-TACs
    return tac_dataframe


folder = 'C:/Users/ф/PycharmProjects/Table_processer/Output/'
lesion_df = pd.read_csv(folder + 'Patient_list.csv', sep=';')

for h in ['ОДГ', 'АнОДГ', 'АСЦ', 'АнАСЦ', 'ГБ', 'Мен', 'Мтс', 'DBCLC']:  # histotypes
    histo = h
    for r in ['Max_uptake_sphere', 'Norma', 'Max_uptake_circle']:  # ROI types
        roi = r
        measure = 'Mean'
        filtered_tac_df = filtered_tac_gen(folder, lesion_df, histo, roi, measure)
        tac_df = curve_percentiles(filtered_tac_df)
