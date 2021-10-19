import pandas as pd


# function for load information from csv with VOI info
def voi_loader(folder_path, file_number):
    path = folder_path
    file = "{0:0=3d}".format(file_number) + ".csv"
    voi_dataframe = pd.read_csv(path + file, sep=' ')
    return voi_dataframe


# function for VOI choosing
def voi_choose(dataframe, voi):
    df = dataframe[dataframe.ROI == voi]
    return df


# function for sorting VOI info into separate csv files
def voi_separation(patient_number, voi_df):
    # delete CT information and last strings
    voi_df = voi_df[voi_df.Volume != 'CT - CT 3.27 mm']
    voi_df = voi_df[voi_df.ROI != 'PERCIST 1.0']

    # generating the list of VOI
    voi_list = pd.Series(voi_df['ROI']).unique()

    # Particular VOI dataframes generation
    for j in range(len(voi_list)):
        voi_df_nw = voi_choose(voi_df, voi_list[j])

        # generating a new data frame with limited VOI info
        voi_supp_info = voi_df_nw[voi_df_nw.Stat == 'Макс'][['Patient Name', 'Volume', 'ROI']].reset_index()
        del voi_supp_info['index']

        voi_max = voi_df_nw[voi_df_nw.Stat == 'Макс'][['Value']].reset_index()
        del voi_max['index']
        voi_mean = voi_df_nw[voi_df_nw.Stat == 'Средн.'][['Value']].reset_index()
        del voi_mean['index']
        voi_peak = voi_df_nw[voi_df_nw.Stat == 'Пик'][['Value']].reset_index()
        del voi_peak['index']

        voi_df_nw = pd.DataFrame({
            'Series': voi_supp_info.Volume,
            'VOI': voi_supp_info.ROI,
            'Maximum': voi_max.Value,
            'Mean': voi_mean.Value,
            'Peak': voi_peak.Value
        })

        voi_name = patient_number + '_' + voi_list[j] + '.csv'
        print(voi_name)
        return voi_df_nw.to_csv(voi_name, sep='\t')


# VOI info load in dataframe
path_to_vois_folder = 'C:/Kotomin/Globalall/Methionine_dyn/02_TAC/VOI_TACs/'

for i in range(2):
    file_num = i + 1
    patient_num = "{0:0=3d}".format(file_num)
    voi_df_unsort = voi_loader(path_to_vois_folder, file_num)
    voi_separation(patient_num, voi_df_unsort)
