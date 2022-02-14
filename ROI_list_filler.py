import pandas as pd

roi_list = pd.read_csv('C:/Users/ф/PycharmProjects/Table_processer/ROI_list.csv', sep=';', dtype={'Lesion': str})
del roi_list['Index']

for i in range(715, 755):
    roi_list.loc[3 * i + 2] = ["{0:0=3d}".format(i), 'ROI 1 - Free Hand', 'Norma']
    roi_list.loc[3 * i + 3] = ["{0:0=3d}".format(i), 'ROI 2 - Sphere', 'Max_uptake_sphere']
    roi_list.loc[3 * i + 4] = ["{0:0=3d}".format(i), 'ROI 3 - 2D Ellipse', 'Max_uptake_circle']

roi_list.to_csv('ROI_list1.csv', sep=';')
