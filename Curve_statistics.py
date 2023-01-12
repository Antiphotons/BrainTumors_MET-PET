import os.path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from numpy import percentile, mean, std, triu, ones_like
from scipy.stats import sem


# function to generate median & percentile curves from TACs
def curve_average(tac_df, central_meas):
    y_df = tac_df.drop(columns='Time')
    if central_meas == 'Median':
        average = [percentile(y_df.loc[i], 50) for i in range(len(tac_df.Time))]  # median
        low_limit = [percentile(y_df.loc[i], 2.5) for i in range(len(tac_df.Time))]  # 1 quartile
        high_limit = [percentile(y_df.loc[i], 97.5) for i in range(len(tac_df.Time))]  # 3 quartile
    elif central_meas == 'Mean':
        average = [mean(y_df.loc[i]) for i in range(len(tac_df.Time))]  # mean
        low_limit = [mean(y_df.loc[i]) - std(y_df.loc[i]) * 1.96 for i in range(len(tac_df.Time))]  # -1.96 SD
        high_limit = [mean(y_df.loc[i]) + std(y_df.loc[i]) * 1.96 for i in range(len(tac_df.Time))]  # +1.96 SD
    elif central_meas == 'CI95':
        average = [mean(y_df.loc[i]) for i in range(len(tac_df.Time))]  # mean
        low_limit = [mean(y_df.loc[i]) - sem(y_df.loc[i]) * 1.96 for i in range(len(tac_df.Time))]  # -1.96 SE
        high_limit = [mean(y_df.loc[i]) + sem(y_df.loc[i]) * 1.96 for i in range(len(tac_df.Time))]  # +1.96 SE

    tac_df['Average'], tac_df['Low_limit'], tac_df['High_limit'] = average, low_limit, high_limit
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


# function for reorganise 31-frame TAC to 26-frame TAC
def tac_transformer(tac_df, measure_type):
    if len(tac_df.Time) == 31:

        # 120-sec-frames to 180-sec-frames
        nw_tac_df = pd.DataFrame(columns=['Time', measure_type])
        for i in range(0, 16):
            nw_tac_df.loc[i] = tac_df.loc[i]
        cnt = 0
        for i in range(16, 31, 3):
            nw_tac_df.loc[i - cnt, measure_type] = sum(tac_df[measure_type].loc[i:i + 1]) / 2
            nw_tac_df.loc[i - cnt, 'Time'] = tac_df.loc[i, 'Time']
            nw_tac_df.loc[i + 1 - cnt, measure_type] = sum(tac_df[measure_type].loc[i + 1:i + 2]) / 2
            nw_tac_df.loc[i + 1 - cnt, 'Time'] = tac_df.loc[i, 'Time'] + 180
            cnt += 1
        nw_tac_df = nw_tac_df.reset_index(drop=True)
    else:
        nw_tac_df = tac_df
    return nw_tac_df


# function for generate dataframe consist of TACs of specific histotype, measure and roi
def filtered_tac_gen(folder_path, lesion_dataframe, histotype, roi, measure_type):
    filtr_lesion_df = lesion_dataframe[lesion_dataframe.Histo == histotype]
    filtr_lesion_df = filtr_lesion_df.reset_index(drop=True)
    tac_df = pd.DataFrame(columns=['Time'])

    for i in range(len(filtr_lesion_df.Les)):
        filename = "{0:0=3d}".format(filtr_lesion_df.Les[i]) + '_' + roi + '.csv'
        if os.path.exists(folder_path + filename):  # checking if a ROI file exists
            tac = curve_loader(folder_path, filename, measure_type)
            tac = tac_smoother(tac, measure_type)  # transform 70-frame-TACs
            tac = tac_conditioner(tac, measure_type)  # replace time points and generate first zero frame
            tac = tac_transformer(tac, measure_type)  # transform 31-frame-TACs to 26-frame-TACs
            tac_df.Time = tac.Time
            tac_df[filename] = tac[measure_type]
    return tac_df


# function for filtering and sorting of csv with clinical and demographic data
def patient_list_sort(folder_path, lesion_dataframe):
    nw_lesion_df = pd.DataFrame(columns=lesion_dataframe.columns)
    for i in range(len(lesion_dataframe.Les)):
        filename = "{0:0=3d}".format(lesion_dataframe.Les[i]) + '.csv'
        if os.path.exists(folder_path + filename):  # checking if a ROI file exists
            nw_lesion_df = pd.concat([nw_lesion_df, lesion_dataframe.iloc[i].to_frame().T], ignore_index=True)
            nw_lesion_df = nw_lesion_df.sort_values(by='Les')
    nw_lesion_df.to_csv('Patient_list_sorted.csv', '\t')


# function for computation coefficient of linear regression
def slope(x, y):
    return x.cov(y) / x.var()


# function for computation intercept of linear regression
def intercept(x, y):
    return y.mean() - (x.mean() * slope(x, y))


# function for plotting time-activity curve
def tac_plot(tac_df, filename, measure_type):
    time, activity = pd.Series.tolist(tac_df['Time']), pd.Series.tolist(tac_df['Average'])
    # first, second = pd.Series.tolist(tac_df['019_Max_uptake_sphere.csv']),
    # pd.Series.tolist(tac_df['070_Max_uptake_sphere.csv'])
    l_lim, h_lim = pd.Series.tolist(tac_df['Low_limit']), pd.Series.tolist(tac_df['High_limit'])
    reg_line = [slope(tac_df[tac_df.Time >= 600]['Time'], tac_df[tac_df.Time >= 600]['Average']) * t +
                intercept(tac_df[tac_df.Time >= 600]['Time'], tac_df[tac_df.Time >= 600]['Average']) for t in time]
    late_phase = time.index(690)
    plt.figure(figsize=(12, 4))
    # plt.plot(time, first, time, second)
    plt.plot(time, activity)
    ax = plt.subplot()
    ax.fill_between(time, l_lim, h_lim, color='m', alpha=.1)
    plt.xlabel('Time (sec)')
    if measure_type in ['Mean', 'Maximum', 'Peak']:
        plt.ylabel('SUVbw ' + measure_type)  # for SUV curves
    else:
        plt.ylabel(measure_type)  # for TBR curves
    plt.savefig(filename + '_' + measure_type.lower() + '.png')


# function for plotting multiple time-activity curves
def tac_multiplot(tacs_df, measure_type):
    time = pd.Series.tolist(tacs_df['', 'Time'])
    plt.figure(figsize=(12, 4))
    for h in range(0, len(tacs_df.columns) - 1, 3):
        activity = pd.Series.tolist(tacs_df[tacs_df.columns[h]])
        l_lim = pd.Series.tolist(tacs_df[tacs_df.columns[h+1]])
        h_lim = pd.Series.tolist(tacs_df[tacs_df.columns[h+2]])
        ax, ax1 = plt.subplot(), plt.subplot()
        ax.plot(time, activity)
        ax1.fill_between(time, l_lim, h_lim, alpha=.1)

    plt.savefig('Multiplot.png')


# function for generating correlation heatmap half-matrix
def correlation_heatmap(path):
    sns.set_theme(style="white")

    # Load dataset
    d = pd.read_csv(path, sep='\t')
    del d['Unnamed: 0']

    # Compute the correlation matrix
    corr = d.corr()
    print(corr)

    # Generate a mask for the upper triangle
    mask = triu(ones_like(corr, dtype=bool))

    # Set up the matplotlib figure
    f, ax = plt.subplots(figsize=(11, 20))

    # Generate a custom diverging colormap
    cmap = sns.diverging_palette(230, 20, as_cmap=True)

    # Draw the heatmap with the mask and correct aspect ratio
    sns.heatmap(corr, mask=mask, cmap=cmap, vmax=1, center=0,
                square=True, linewidths=.5, cbar_kws={"shrink": .5})
    plt.show()


folder = 'C:/PycharmProjects/Table_processer/Output/'
lesion_df = pd.read_csv(folder + 'Patient_list.csv', sep='\t')  # load df with hystotypes

# possible variables
histotypes = ['ОДГ', 'АСЦ', 'АнАСЦ', 'ГБ', 'АнОДГ', 'Мен', 'Мтс', 'DBCLC']
rois = ['Max_uptake_sphere', 'Norma', 'Max_uptake_circle']
uptake_unit_types = ['Mean', 'Maximum', 'TBR_Mean', 'TBR_Maximum']
central_statistics = ['Median', 'Mean', 'CI95']
stats = ['Average', 'Low_limit', 'High_limit']

# df for multiple histotype curve plot
iterables = [histotypes[0:2], stats]  # set required hystotypes
multindex = pd.MultiIndex.from_product(iterables, names=['Histotype', 'Stats'])
all_hys_tacs = pd.DataFrame(columns=multindex)  # generate dataframe

for h in range(8):  # set histotype
    histo = histotypes[h]
    for r in range(0, 1):  # set ROI type
        roi = rois[r]
        for m in range(1):  # set uptake unit type
            measure = uptake_unit_types[m]
            average = central_statistics[2]  # set type of central statistics and corresponding limits
            #filtered_tac_df = filtered_tac_gen(folder, lesion_df, histo, roi, measure)  # df with hystospecific TACs
            #tac_w_average = curve_average(filtered_tac_df, average)  # add average TAC with limits to df
            #tac_plot(tac_w_average, histo + '_' + roi, measure)  # tac plot draw
            #for stat in stats:
                #all_hys_tacs[(histo, stat)] = tac_w_average[stat]
#all_hys_tacs[('', 'Time')] = tac_w_average['Time']
#tac_multiplot(all_hys_tacs, uptake_unit_types[0])
#patient_list_sort(folder, lesion_df)
correlation_heatmap('C:/PycharmProjects/Table_processer/Curve_stats.csv')