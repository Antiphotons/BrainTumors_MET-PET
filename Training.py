# print(voi_df.iloc[1]) example of indexation

import pandas as pd


# function for load information from csv with VOI info
def voi_loader(folder_path, file_number):
    path = folder_path
    file = "{0:0=3d}".format(file_number) + ".csv"
    voi_dataframe = pd.read_csv(path + file, sep=' ')
    return voi_dataframe

# VOI info load in dataframe
path_to_vois_folder = 'C:/Kotomin/Globalall/Methionine_dyn/02_TAC/VOI_TACs/'

for i in range(2):
    file_num = i + 1
    voi_df = voi_loader(path_to_vois_folder, file_num)
    print(voi_df)