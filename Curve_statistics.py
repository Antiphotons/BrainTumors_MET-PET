import os.path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


# function to generate median & percentile curves from TACs
def curve_percentiles(tac_df):
    y_df = tac_df.drop(columns='Time')
    median = [np.percentile(y_df.loc[i], 50) for i in range(len(tac_df.Time))]
    low_percentile = [np.percentile(y_df.loc[i], 5) for i in range(len(tac_df.Time))]
    high_percentile = [np.percentile(y_df.loc[i], 95) for i in range(len(tac_df.Time))]
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
            nw_tac_df.loc[i - cnt, 'Time'] = tac_df.loc[i, 'Time']
            nw_tac_df.loc[i + 1 - cnt, measure_type] = sum(tac_df[measure_type].loc[i + 1:i + 2]) / 2
            nw_tac_df.loc[i + 1 - cnt, 'Time'] = tac_df.loc[i, 'Time'] + 180
            cnt += 1
        nw_tac_df = nw_tac_df.reset_index()
        del nw_tac_df['index']
    else:
        nw_tac_df = tac_df
    return nw_tac_df


# function for generate dataframe consist of TACs of specific histotype, measure and roi
def filtered_tac_gen(folder_path, lesion_dataframe, histotype, roi, measure_type):
    filtr_lesion_df = lesion_dataframe[lesion_dataframe.Histo == histotype]
    filtr_lesion_df = filtr_lesion_df.reset_index()
    del filtr_lesion_df['index']
    tac_df = pd.DataFrame(columns=['Time'])

    for i in range(len(filtr_lesion_df.Les)):
        filename = "{0:0=3d}".format(filtr_lesion_df.Les[i]) + '_' + roi + '.csv'
        if os.path.exists(folder_path + filename):  # checking if a ROI file exists
            tac = curve_loader(folder_path, filename, measure_type)
            tac = tac_smoother(tac, measure_type)  # transform 70-frame-TACs
            tac = tac_transformer(tac, measure_type)  # transform 30-frame-TACs to 25-frame-TACs
            tac_df.Time = tac.Time
            tac_df[filename] = tac[measure_type]
    return tac_df


# function for computation coefficient of linear regression
def slope(x, y):
    return x.cov(y) / x.var()


# function for computation intercept of linear regression
def intercept(x, y):
    return y.mean() - (x.mean() * slope(x, y))


# function for plotting time-activity curve
def tac_plot(tac_df, filename, measure_type):
    time, activity = pd.Series.tolist(tac_df['Time']), pd.Series.tolist(tac_df['Median'])
    first, second = pd.Series.tolist(tac_df['019_Max_uptake_sphere.csv']), pd.Series.tolist(tac_df['070_Max_uptake_sphere.csv'])
    l_perc, h_perc = pd.Series.tolist(tac_df['Low_percentile']), pd.Series.tolist(tac_df['High_percentile'])
    reg_line = [slope(tac_df[tac_df.Time >= 600]['Time'], tac_df[tac_df.Time >= 600]['Median']) * t +
                intercept(tac_df[tac_df.Time >= 600]['Time'], tac_df[tac_df.Time >= 600]['Median']) for t in time]
    late_phase = time.index(600)
    plt.figure(figsize=(12, 4))
    plt.plot(time, first, time, second)
    #ax = plt.subplot()
    #ax.fill_between(time, l_perc, h_perc, color='m', alpha=.1)
    plt.xlabel('Time (sec)')
    plt.ylabel(measure_type + ' (SUVbw)')
    plt.savefig(filename + '_' + measure_type.lower() + '.png')


folder = 'C:/Users/ф/PycharmProjects/Table_processer/Output/'
lesion_df = pd.read_csv(folder + 'Patient_list.csv', sep='\t')

for h in ['АнОДГ']: #['ОДГ', 'АнОДГ', 'АСЦ', 'АнАСЦ', 'ГБ', 'Мен', 'Мтс', 'DBCLC']:  # histotypes
    histo = h
    for r in ['Max_uptake_sphere']:
        #'Max_uptake_sphere', 'Norma', 'Max_uptake_circle']:  # ROI types
        roi = r
        measure = 'Maximum'
        filtered_tac_df = filtered_tac_gen(folder, lesion_df, histo, roi, measure)
        tac_with_perc = curve_percentiles(filtered_tac_df)
        tac_plot(tac_with_perc, histo + '_' + roi, measure)  # tac plot draw
