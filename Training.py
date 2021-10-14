import pandas as pd

voi_df = pd.read_csv('C:/Kotomin/Globalall/Methionine_dyn/02_TAC/VOI_TACs/SkrynnikovVA_all.csv', sep=',')
voi_df = voi_df[voi_df.Volume != 'CT - CT 3.27 mm']
voi_data = voi_df[voi_df.Stat == 'Макс'][['Patient Name', 'Volume', 'ROI', 'Stat', 'Value']].reset_index()
del voi_data['index']

print(voi_data)