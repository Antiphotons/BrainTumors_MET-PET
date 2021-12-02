import os.path
import pandas as pd
import matplotlib.pyplot as plt
import math as m


# function for transform VOI file to curve dataframe
def curve_loader(folder_path, file_name, measure_type):
    path = folder_path
    file = file_name  # input from user before function starts
    voi_dataframe = pd.read_csv(path + file, sep='\t')  # previous created VOI .csv
    # only dynamic data preserved
    voi_dataframe = voi_dataframe[voi_dataframe.Series != 'PET - 10-30'].reset_index()
    # detect type of curve (25 or 70 frames)
    if len(voi_dataframe.VOI) < 26:
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


# function for plotting time-activity curve
def tac_plot(tac_df, filename, measure_type):
    time, activity = pd.Series.tolist(tac_df['Time']), pd.Series.tolist(tac_df[measure_type])
    plt.figure(figsize=(12, 4))
    plt.plot(time, activity)
    plt.xlabel('Time (sec)')
    plt.ylabel(measure_type + ' (SUVbw)')
    plt.savefig(filename + '_' + measure_type.lower() + '.png')


# function for computation TAC statistics
def tac_stat(tac_df, measure_type):
    tac_max = max(tac_df[measure_type])  # maximal SUV on curve
    tac_max_ep = max(tac_df[tac_df.Time < 600][measure_type])  # maximum in early phase (0-10 min)
    tac_max_lp = max(tac_df[tac_df.Time >= 600][measure_type])  # maximum in late phase (>10 min)
    t_max = tac_df.Time[tac_df[tac_df[measure_type] == tac_max].index[-1]]  # time of maximal SUV
    t_max_ep = tac_df.Time[tac_df[tac_df[measure_type] == tac_max_ep].index[-1]]
    t_max_lp = tac_df.Time[tac_df[tac_df[measure_type] == tac_max_lp].index[-1]]
    tac_char = [tac_max, t_max, tac_max_ep / t_max_ep * 60]  # string of TAC characteristics
    return tac_char


folder = 'C:/Users/ф/PycharmProjects/Table_processer/'

for roi in ['Max_uptake_sphere', 'Norma', 'Max_uptake_circle']:  # ROI types
    roi_tbl = pd.DataFrame(columns=['Lesion', 'Peak', 'TTP', 'Slope_early'])

    for i in range(3):  # number of lesions in working directory
        file = "{0:0=3d}".format(i + 1) + '_' + roi  # filename without extension for plots naming
        file_with_ext = file + '.csv'  # filename with extension for a file opening
        if os.path.exists(folder + file_with_ext):  # checking if a ROI file exists
            tac = curve_loader(folder, file_with_ext, 'Mean')  # tac dataframe load
            # tac_plot(tac, file, 'Mean')  # tac plot draw
            roi_tbl.loc[i] = ["{0:0=3d}".format(i + 1)] + tac_stat(tac, 'Mean')  # addition TAC statistics to table
    roi_tbl.to_csv(roi + '.csv', sep='\t')
