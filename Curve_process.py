import os.path
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker


# function for transform VOI file to curve dataframe
def curve_loader(folder_path, file_name, measure_type):
    path = folder_path
    file = file_name  # input from user before function starts
    voi_dataframe = pd.read_csv(path + file, sep='\t')  # previous created VOI .csv
    # only dynamic data preserved
    voi_dataframe = voi_dataframe[voi_dataframe['Series'].str.contains('Dynamic')].reset_index(drop=True)
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
        measure_type: voi_dataframe[measure_type],  # type of activity value (mean, max, peak or TBR)
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


# function for addition to TAC first frame with zero value and shift times to the frame center
def tac_conditioner(tac_df, measure_type):

    # shift times to the center of the correspondent frames

    # compute last time point in the center between last real point and virtual next
    last_timepoint = (tac_df.Time[len(tac_df.Time) - 1] * 3 - tac_df.Time[len(tac_df.Time) - 2]) / 2
    # compute new time points between previous
    for i in range(len(tac_df.Time) - 1):
        tac_df.loc[i, 'Time'] = (tac_df.loc[i, 'Time'] + tac_df.loc[i+1, 'Time']) / 2
    tac_df.loc[len(tac_df.Time) - 1, 'Time'] = last_timepoint  # resolve problem with out of range index

    # add zero value in -15 second time point
    new_tac_df = pd.DataFrame({measure_type: [0], 'Time': [-15]})  # new TAC df with single zero time point
    new_tac_df = pd.concat([new_tac_df, tac_df], ignore_index=True)  # merge new and general TAC
    return new_tac_df


# function for computation coefficient of linear regression
def slope(x, y):
    return x.cov(y) / x.var()


# function for computation intercept of linear regression
def intercept(x, y):
    return y.mean() - (x.mean() * slope(x, y))


# function for plotting time-activity curve
def tac_plot(tac_df, filename, measure_type):
    time, activity = pd.Series.tolist(tac_df['Time']), pd.Series.tolist(tac_df[measure_type])

    # line of linear regression
    reg_line = [slope(tac_df[tac_df.Time >= 600]['Time'], tac_df[tac_df.Time >= 600][measure_type]) * t +
                intercept(tac_df[tac_df.Time >= 600]['Time'], tac_df[tac_df.Time >= 600][measure_type]) for t in time]
    late_phase = time.index(570) + 1  # cut-off of late phase
    plt.figure(figsize=(12, 4))
    ax = plt.subplot()
    plt.grid(True)
    plt.plot(time, activity, time[late_phase:], reg_line[late_phase:], 'r--', linewidth=2)
    plt.axis([-30, 2400, 0, max(activity) + 0.5])  # axes limits
    ax.xaxis.set_major_locator(ticker.MultipleLocator(180))  # major x axis devision (ticks)
    ax.xaxis.set_minor_locator(ticker.MultipleLocator(60))  # minor x axis devision (ticks)
    if max(activity) <= 7.0:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(0.5))  # major y axis devision (ticks)
    else:
        ax.yaxis.set_major_locator(ticker.MultipleLocator(1))  # major y axis devision (ticks)
    plt.xlabel('Time (sec)')
    if measure_type in ['Mean', 'Maximum', 'Peak']:
        plt.ylabel('SUVbw ' + measure_type)  # for SUV curves
    else:
        plt.ylabel(measure_type)  # for TBR curves
    plt.savefig(filename + '_' + measure_type.lower() + '.png')


# function for computation TAC statistics
def tac_stat(tac_df, measure_type):
    tac_max = max(tac_df[measure_type])  # maximal SUV on curve
    tac_max_ep = max(tac_df[tac_df.Time < 600][measure_type])  # maximum in early phase (0-10 min)
    tac_max_lp = max(tac_df[tac_df.Time >= 600][measure_type])  # maximum in late phase (>10 min)
    tac_max_60 = max(tac_df[tac_df.Time <= 60][measure_type])  # maximum in initial phase (0-1 min)
    t_max = tac_df.Time[tac_df[tac_df[measure_type] == tac_max].index[-1]]  # time of maximal SUV or TBR
    t_max_ep = tac_df.Time[tac_df[tac_df[measure_type] == tac_max_ep].index[-1]]
    t_max_lp = tac_df.Time[tac_df[tac_df[measure_type] == tac_max_lp].index[-1]]
    b1 = slope(tac_df[tac_df.Time >= 600]['Time'], tac_df[tac_df.Time >= 600][measure_type])  # slope
    # string of TAC characteristics
    tac_char = [round(tac_max, 2), round(tac_max_60, 2), t_max, t_max_lp,
                round(tac_max_ep / t_max_ep * 3600, 2), round(b1 * 3600, 3)]
    return tac_char


folder = 'C:/PycharmProjects/Table_processer/Output/'

for roi in ['Max_uptake_circle', 'Max_uptake_sphere', 'Norma']:  # ROI types
    for meas in ['Mean', 'Maximum', 'TBR_Mean', 'TBR_Maximum']:  # measure types
        if roi == 'Max_uptake_circle' and meas in ['Maximum', 'TBR_Maximum']:  # skip nonexistent data
            continue
        elif roi == 'Norma' and meas not in ['Mean']:
            continue

        roi_tbl = pd.DataFrame(columns=['Lesion', 'Peak', 'Peak_60', 'TTP', 'TTP_late',
                                        'Slope_early', 'Slope_late', 'TBR_10-30'])
        for i in range(0, 99):  # number of lesions in working directory
            file = "{0:0=3d}".format(i + 1) + '_' + roi  # filename without extension for plots naming
            file_w_ext = file + '.csv'  # filename with extension for a file opening
            if os.path.exists(folder + file_w_ext):  # checking if a ROI file exists
                print(file + ' - ' + meas)
                tac = curve_loader(folder, file_w_ext, meas)  # tac dataframe load
                tac = tac_smoother(tac, meas)  # transform 70-frame-TACs
                tac = tac_conditioner(tac, meas)  # postprocess TAC
                # tac_plot(tac, file, meas)  # tac plot draw
                if roi != 'Norma':
                    df_st_tbr = pd.read_csv(folder + file_w_ext, sep='\t')
                    st_tbr = [df_st_tbr.loc[len(df_st_tbr) - 1, 'TBR_Mean']]
                    roi_tbl.loc[i] = ["{0:0=3d}".format(i + 1)] + tac_stat(tac, meas) + st_tbr  # add TAC statistics
                else:
                    roi_tbl.loc[i] = ["{0:0=3d}".format(i + 1)] + tac_stat(tac, meas) + ['unsuitable']

        roi_tbl.to_csv(roi + '_' + meas + '.csv', sep='\t')
