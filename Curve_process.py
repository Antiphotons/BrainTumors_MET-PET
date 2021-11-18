import pandas as pd
import math as m


# function for convert kBq/ml to g/ml SUVbw
def suv_converter(activity, weight, value):
    return value * weight / activity


# function for transform VOI file to curve dataframe
def curve_loader(folder_path, file_name, measure_type):
    path = folder_path
    file = file_name  # input from user before function starts
    voi_dataframe = pd.read_csv(path + file, sep='\t')  # previous created VOI .csv
    # only dynamic data preserved
    voi_dataframe = voi_dataframe[voi_dataframe.Series != 'PET - 10-30'].reset_index()
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
    curve_dataframe = voi_dataframe[measure_type]
