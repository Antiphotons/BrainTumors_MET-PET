import pandas as pd


# function for load information from csv with VOI info
def voi_loader(folder_path, file_number):
    path = folder_path
    file = "{0:0=3d}".format(file_number) + ".csv"
    voi_dataframe = pd.read_csv(path + file, sep=',')
    return voi_dataframe


# function for VOI choosing
def voi_choose(dataframe, voi):
    df = dataframe[dataframe.ROI == voi]
    return df


# function to convert kBq/ml to g/ml SUVbw
def suv_converter(path, patient, values):
    # Load table with patient weights & activities
    injection = pd.read_csv(path + 'for_SUV.csv', sep=' ',
                            dtype={'lesion_number': str, 'weight': int, 'activity': float})
    lesion_string = injection[injection.lesion_number == patient].reset_index()
    weight = lesion_string.weight[0]
    activity = lesion_string.activity[0] * 37
    return values * weight / activity


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
        voi_supp_info = voi_df_nw[voi_df_nw.Stat == 'Макс'][['Patient Name', 'Volume', 'ROI', 'Unit']].reset_index()
        del voi_supp_info['index']

        voi_max = voi_df_nw[voi_df_nw.Stat == 'Макс'][['Value']].reset_index()
        del voi_max['index']
        voi_mean = voi_df_nw[voi_df_nw.Stat == 'Средн.'][['Value']].reset_index()
        del voi_mean['index']
        voi_peak = voi_df_nw[voi_df_nw.Stat == 'Пик'][['Value']].reset_index()
        del voi_peak['index']

        # check for measure units and conversation if units are not SUV
        if voi_df_nw.Unit[0] == 'kBq/ml':
            voi_max = suv_converter(path_to_vois_folder, patient_number, voi_max)
            voi_mean = suv_converter(path_to_vois_folder, patient_number, voi_mean)
            voi_peak = suv_converter(path_to_vois_folder, patient_number, voi_peak)
        elif voi_df_nw.Unit[0] != 'g/ml':
            print('error in unit type in lesion number' + patient_number)  # here lesion num = patient num

        # VOI dataframe assembly
        voi_df_nw = pd.DataFrame({
            'Series': voi_supp_info.Volume,
            'VOI': voi_supp_info.ROI,
            # 'Units': voi_supp_info.Unit
            'Maximum': voi_max.Value,
            'Mean': voi_mean.Value,
            'Peak': voi_peak.Value
        })

        voi_name = patient_number + '_' + voi_list[j] + '.csv'
        print(voi_name)
        voi_df_nw.to_csv(voi_name, sep='\t')


# VOI info load in dataframe
path_to_vois_folder = 'C:/Kotomin/Globalall/Methionine_dyn/02_TAC/VOI_TACs/'

for i in range(3):
    file_num = i + 1
    patient_num = "{0:0=3d}".format(file_num)
    voi_df_unsort = voi_loader(path_to_vois_folder, file_num)
    voi_separation(patient_num, voi_df_unsort)
