import pandas as pd

voi_df = pd.read_csv('C:/Kotomin/Globalall/Methionine_dyn/02_TAC/VOI_TACs/SkrynnikovVA_all.csv', sep=',')   # VOI info load
voi_data = voi_df[['Patient Name', 'Volume', 'ROI', 'Stat', 'Value']]   # generating a new data frame with limited VOI info
# print(voi_df.iloc[1])
# print(curves.loc[[1], ['Stat', 'Value']])
print(voi_data)