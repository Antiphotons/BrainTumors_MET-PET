import pandas as pd

#times = pd.Series([0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210,
#                           225, 240, 255, 270, 285, 300, 315, 330, 345, 360, 375, 390, 405, 420,
#                           435, 450, 465, 480, 495, 510, 525, 540, 555, 570, 585, 600, 630, 660,
#                           690, 720, 750, 780, 810, 840, 870, 900, 930, 960, 990, 1020, 1050, 1080,
#                           1110, 1140, 1170, 1200, 1320, 1440, 1560, 1680, 1800, 1920, 2040, 2160, 2280])
#print(times)
#print(times[times == 240])
#print(times[times == 240].index[0])


def suv_converter(path, patient, values):
    # Load table with patient weights & activities
    injection = pd.read_csv(path + 'for_SUV.csv', sep=' ',
                            dtype={'lesion_number': str, 'weight': int, 'activity': float})
    lesion_string = injection[injection.lesion_number == patient].reset_index()
    weight = lesion_string.weight[0]
    activity = lesion_string.activity[0] * 37
    return values * weight / activity


pathname = 'C:/Users/Ezhiki-Porosenki/PycharmProjects/Table_processer/'
lesion_num = '002'
maximums = pd.Series([7, 8, 9, 10])
maximums = suv_converter(pathname, lesion_num, maximums)
print(maximums)
