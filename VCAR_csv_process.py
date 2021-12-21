import pandas as pd


# function for load information from csv with VOI info
def voi_loader(folder_path, lesion_number):
    path = folder_path
    file = lesion_number + ".csv"
    voi_dataframe = pd.read_csv(path + file, sep=',')
    return voi_dataframe


# function for VOI choosing
def voi_choose(dataframe, voi):
    df = dataframe[dataframe.ROI == voi]
    return df


# function to convert kBq/ml to g/ml SUVbw
def suv_converter(path, lesion, values):
    # Load table with patient weights & activities
    injection = pd.read_csv(path + 'for_SUV.csv', sep=' ',
                            dtype={'lesion_number': str, 'weight': int, 'activity': float})
    lesion_string = injection[injection.lesion_number == lesion].reset_index()
    weight = lesion_string.weight[0]
    activity = lesion_string.activity[0] * 37
    return round(values * weight / activity, 2)


# function for sorting VOI info into separate csv files
def voi_separation(lesion_number, voi_df):
    # delete CT information and garbage strings
    voi_df = voi_df[voi_df.Volume != 'CT - CT 3.27 mm']
    voi_df = voi_df[voi_df.ROI != 'PERCIST 1.0']
    voi_df = voi_df[voi_df.ROI != 'Ссылка на VOI - Sphere']

    # generating the list of VOI
    voi_list = pd.Series(voi_df['ROI']).unique()

    # Particular ROI dataframes generation
    for j in range(len(voi_list)):
        voi_df_nw = voi_choose(voi_df, voi_list[j]).reset_index()  # choosing ROI
        del voi_df_nw['index']

        # generating a new data frame with limited ROI info
        voi_supp_info = voi_df_nw[voi_df_nw.Stat == 'Макс'][['Patient Name', 'Volume', 'ROI', 'Unit']].reset_index()
        del voi_supp_info['index']

        voi_max = voi_df_nw[voi_df_nw.Stat == 'Макс'][['Value']].reset_index()
        del voi_max['index']
        voi_max.Value = pd.to_numeric(voi_max.Value)
        voi_mean = voi_df_nw[voi_df_nw.Stat == 'Средн.'][['Value']].reset_index()
        del voi_mean['index']
        voi_mean.Value = pd.to_numeric(voi_mean.Value)
        voi_peak = voi_df_nw[voi_df_nw.Stat == 'Пик'][['Value']].reset_index()
        del voi_peak['index']
        voi_peak.Value = pd.to_numeric(voi_peak.Value)

        # check for measure units and conversation if units are not SUV
        if voi_supp_info.Unit[0] == 'kBq/ml':
            voi_max.Value = suv_converter(path_to_vois_folder, lesion_number, voi_max.Value)
            voi_mean.Value = suv_converter(path_to_vois_folder, lesion_number, voi_mean.Value)
            voi_peak.Value = suv_converter(path_to_vois_folder, lesion_number, voi_peak.Value)
        elif voi_supp_info.Unit[0] != 'g/ml':
            print('error in unit type in lesion number' + lesion_number)  # here lesion num = patient num

        # VOI dataframe assembly
        voi_df_nw = pd.DataFrame({
            'Series': voi_supp_info.Volume,
            'VOI': voi_supp_info.ROI,
            # 'Units': voi_supp_info.Unit
            'Maximum': voi_max.Value,
            'Mean': voi_mean.Value,
            'Peak': voi_peak.Value
        })

        # Save ROI with usable names
        voi_name_df = pd.read_csv(path_to_vois_folder + 'ROI_list.csv', sep=';', dtype={'Lesion': str})
        voi_name_df = voi_name_df[voi_name_df.Lesion == lesion_number]
        voi_name_df = voi_name_df[voi_name_df.Filename == voi_list[j]]
        voi_name = lesion_number + '_' + voi_name_df.ROI.tolist()[0] + '.csv'
        print(voi_name)
        voi_df_nw.to_csv(voi_name, sep='\t')


# VOI info load in dataframe
path_to_vois_folder = 'C:/Kotomin/Globalall/Methionine_dyn/02_TAC/VOI_TACs/'

for i in range(82, 83):
    lesion_num = "{0:0=3d}".format(i + 1)
    voi_df_unsort = voi_loader(path_to_vois_folder, lesion_num)
    voi_separation(lesion_num, voi_df_unsort)
