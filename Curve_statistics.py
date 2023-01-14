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
def filtered_tac_gen(folder_path, lesion_dataframe, type, group, roi, measure_type):
    if type == 'Hystology':
        filtr_lesion_df = lesion_dataframe[lesion_dataframe.Histo == group]
    elif type == 'Malignance':
        filtr_lesion_df = lesion_dataframe[lesion_dataframe.Mal == group]
    filtr_lesion_df = filtr_lesion_df.reset_index(drop=True)
    tac_df = pd.DataFrame(columns=['Time'])

    for i in range(len(filtr_lesion_df.Les)):
        filename = filtr_lesion_df.Les[i] + '_' + roi + '.csv'
        if os.path.exists(folder_path + filename):  # checking if a ROI file exists
            tac = curve_loader(folder_path, filename, measure_type)
            tac = tac_smoother(tac, measure_type)  # transform 70-frame-TACs
            tac = tac_conditioner(tac, measure_type)  # replace time points and generate first zero frame
            tac = tac_transformer(tac, measure_type)  # transform 31-frame-TACs to 26-frame-TACs
            tac_df.Time = tac.Time
            tac_df[filename] = tac[measure_type]
    return tac_df


# function for filtering and sorting of csv with clinical and demographic data
def patient_list_sort(folder_path, lesion_dataframe, save_option):
    nw_lesion_df = pd.DataFrame(columns=lesion_dataframe.columns)
    for i in range(len(lesion_dataframe.Les)):
        filename = lesion_dataframe.Les[i] + '.csv'
        if os.path.exists(folder_path + filename):  # checking if a ROI file exists
            nw_lesion_df = pd.concat([nw_lesion_df, lesion_dataframe.iloc[i].to_frame().T], ignore_index=True)
            nw_lesion_df = nw_lesion_df.sort_values(by='Les')
    if save_option == 'save':
        nw_lesion_df.to_csv('Patient_list_sorted.csv', '\t')
    return nw_lesion_df


# function for merging clinical data from the patient_list.csv with curve statistics df
def clinic_to_curve(folder_path, stat_file, clin_df, orient='vert'):

    stat_df = pd.read_csv(folder_path + stat_file, sep='\t',
                          dtype={'Lesion': str})  # file with all curve statistics
    clin_df_sort = patient_list_sort(folder_path, clin_df, 'no')  # sort patient_list by Lesion number

    if orient == 'vert':  # vertically-oriented dataframe
        stat_df.reset_index(drop=True)

        # vertically multiplication of clinical dataframe
        if len(stat_df.Lesion) % len(clin_df_sort.Les) != 0:
            print('ERROR: stat df length not multiple of clinical df legth')
        clin_df_nw = pd.DataFrame()
        for _ in range(int(len(stat_df.Lesion) / len(clin_df_sort.Les))):
            clin_df_nw = pd.concat([clin_df_nw, clin_df_sort], axis=0)
        clin_df_sort = clin_df_nw.reset_index(drop=True)

    if orient == 'hor':  # horizontally-oriented dataframe

        stat_df.index = stat_df.Lesion
        clin_df_sort = patient_list_sort(folder_path, clin_df, 'no')  # sort patient_list by Lesion number
        clin_df_sort.index = clin_df_sort['Les']  # set Lesion number as index
        clin_df_sort.index.rename('Lesion')

    both_df = pd.concat([stat_df, clin_df_sort], axis=1)  # merge data
    return both_df


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
    plt.figure(figsize=(9, 4))
    for h in range(0, len(tacs_df.columns) - 1, 3):
        activity = pd.Series.tolist(tacs_df[tacs_df.columns[h]])
        l_lim = pd.Series.tolist(tacs_df[tacs_df.columns[h+1]])
        h_lim = pd.Series.tolist(tacs_df[tacs_df.columns[h+2]])
        ax, ax1 = plt.subplot(), plt.subplot()
        ax.plot(time, activity, label=tacs_df.columns[h][0] + 'качественные')
        ax1.fill_between(time, l_lim, h_lim, alpha=.1)
    plt.xlabel('Time (sec)')
    if measure_type in ['Mean', 'Maximum', 'Peak']:
        plt.ylabel('SUVbw ' + measure_type + ' (g/ml)')  # for SUV curves
    else:
        plt.ylabel(measure_type)  # for TBR curves
    plt.legend(loc='lower right')
    plt.savefig('Ben_and_mal_' + measure_type + '.png')


# function for generating correlation heatmap half-matrix
def correlation_heatmap(path):
    sns.set_theme(style="white")

    # Load dataset
    d = pd.read_csv(path, sep='\t')
    del d['Unnamed: 0']

    # Compute the correlation matrix
    corr = d.corr()

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


# function for plotting violin plots for curve statistics
def violin_plot(dataframe, group_type, groups, cv_chars, measure, roi):
    sns.set_theme(style="whitegrid", font_scale=1.2)
    curve_dict = {
        'Max_uptake_sphere_Mean': 'SUVsph',
        'Max_uptake_sphere_Maximum': 'SUVmax',
        'Max_uptake_sphere_TBR_Mean': 'TBRsph',
        'Max_uptake_sphere_TBR_Maximum': 'TBRmax',
        'Max_uptake_circle_Mean': 'SUVcrc',
        'Max_uptake_circle_TBR_Mean': 'TBRcrc'
    }

    # filter rows with needed group labels
    df_g, df_r, df_m, df = pd.DataFrame(), pd.DataFrame(), pd.DataFrame(), pd.DataFrame()
    for g in groups:  # filter needed groups
        df_part = dataframe[dataframe[group_type] == g]
        df_g = pd.concat([df_g, df_part])  # df with needed groups only
    for r in roi:  # filter needed ROIs
        df_part = df_g[df_g['ROI'] == r]
        df_r = pd.concat([df_r, df_part])  # df with needed groups and ROIs only
    for m in measure:  # filter needed uptake units
        df_part = df_r[df_r['Meas'] == m]
        df_m = pd.concat([df_m, df_part])  # df with needed groups, units and ROIs only
    for cv in cv_chars:
        df_part = df_m[df_m['CvMeas'] == cv]
        df = pd.concat([df, df_part])  # df with needed curve measures, groups, units and ROIs only

    # create new column with curve & measure (ROI + uptake unit + curve characteristic)
    df['Curve_char'] = df['ROI'] + '_' + df['Meas'] + '_' + df['CvMeas']

    # create x labels
    curves = [df['ROI'].tolist()[i] + '_' + df['Meas'].tolist()[i] for i in range(len(df['ROI']))]
    curves = pd.Series(curves).unique()  # list of actual curves
    xlabels = [curve_dict[c] for c in curves] * len(cv_chars)

    f, ax = plt.subplots(figsize=(11, 6))
    sns.violinplot(data=df, x='Curve_char', y='Value', hue=group_type,
                   cut=0, split=True, scale='width', bw=.25, color="r")

    # sns.swarmplot(data=df, x='Curve', y=cv_stats, hue=group_type, palette='Set3')
    # sns.swarmplot(data=df, x='Curve', y='Peak_60', hue=group_type)

    # sns.violinplot(data=df, x='Curve', y='TBR_10-30', hue=group_type, cut=0, split=True, scale='width')
    # sns.boxplot(data=df, x='Curve', y=cv_stats, hue=group_type, dodge=True)
    # sns.stripplot(data=df, color='.3')

    ax.set_xticklabels(xlabels)
    ax.set_xlabel(cv_chars[0] + '                          ' + cv_chars[1] + '                          ' + cv_chars[2])
    plt.legend(loc='upper right')
    sns.despine(left=True, bottom=True)  # remove borders
    plt.show()


folder = 'C:/PycharmProjects/Table_processer/Output/'  # work folder
lesion_df = pd.read_csv(folder + 'Patient_list.csv', sep='\t', dtype={'Les': str})  # load df with clin data

# possible variables
histotypes = ['ОДГ', 'АСЦ', 'АнАСЦ', 'ГБ', 'АнОДГ', 'Мен', 'Мтс', 'ДБКЛ']
malignance = ['добро', 'зло']

rois = ['Max_uptake_sphere', 'Norma', 'Max_uptake_circle']
uptake_unit_types = ['Mean', 'Maximum', 'TBR_Mean', 'TBR_Maximum']
central_statistics = ['Median', 'Mean', 'CI95']
stats = ['Average', 'Low_limit', 'High_limit']
groups = [histotypes, malignance]

# df for multiple histotype curve plot
iterables = [groups[1][:], stats]  # set required group and subgroup types
multindex = pd.MultiIndex.from_product(iterables, names=['Groups', 'Stats'])
all_gr_tacs = pd.DataFrame(columns=multindex)  # generate dataframe


# plot averaged TAC for particular group (histology or malignance)

for g in range(2):
    group = groups[1][g]  # set subgroup of selected group
    for r in range(2, 3):  # set ROI type
        roi = rois[r]
        for m in range(1):  # set uptake unit type
            measure = uptake_unit_types[m]
            average = central_statistics[0]  # set type of central statistics and corresponding limits
            # create df with group-specific TACs
            filtered_tac_df = filtered_tac_gen(folder, lesion_df, 'Malignance', group, roi, measure)
            tac_w_average = curve_average(filtered_tac_df, average)  # add average TAC with limits to df
            # tac_plot(tac_w_average, group + '_' + roi, measure)  # single-group average tac plot draw
            for stat in stats:
                all_gr_tacs[(group, stat)] = tac_w_average[stat]
# all_gr_tacs[('', 'Time')] = tac_w_average['Time']
# tac_multiplot(all_gr_tacs, measure)  # multiple-group average tac plot
# patient_list_sort(folder, lesion_df, 'save')  # sort lesion dataframe by lesion numbers
# correlation_heatmap('C:/PycharmProjects/Table_processer/All_stats_sort.csv')

curve_stats = ['Peak', 'Peak_60', 'TTP', 'TTP_late', 'Slope_early', 'Slope_late', 'TBR_10-30']
if 1 == 2:
    both_df = clinic_to_curve(folder, 'All_stats.csv', lesion_df, 'hor')  # merge clinical and curve statistics data)
    violin_plot(both_df, 'Mal', malignance, curve_stats[4:6], uptake_unit_types[0:3], [rois[0]])
if 1 == 1:
    both_df = clinic_to_curve(folder, 'All_stats_vertical.csv', lesion_df, 'vert')
    violin_plot(both_df, 'Mal', malignance, curve_stats[0:2] + curve_stats[6:7], uptake_unit_types[:], rois[0:1])



