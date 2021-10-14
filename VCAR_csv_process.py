import pandas as pd

# VOI info load
voi_df = pd.read_csv('C:/Kotomin/Globalall/Methionine_dyn/02_TAC/VOI_TACs/SkrynnikovVA_all.csv', sep=',')
# delete CT information
voi_df = voi_df[voi_df.Volume != 'CT - CT 3.27 mm']
# generating a new data frame with limited VOI info
voi_data = voi_df[voi_df.Stat == 'Макс'][['Patient Name', 'Volume', 'ROI', 'Stat', 'Value']].reset_index()
del voi_data['index']

# print(voi_df.iloc[1])
# print(curves.loc[[1], ['Stat', 'Value']])

voi_max = voi_df[voi_df.Stat == 'Макс'][['Value']].reset_index()
del voi_max['index']
voi_mean = voi_df[voi_df.Stat == 'Средн.'][['Value']].reset_index()
del voi_mean['index']
voi_peak = voi_df[voi_df.Stat == 'Пик'][['Value']].reset_index()
del voi_peak['index']

example = pd.DataFrame({
    'Series': voi_data.Volume,
    'VOI': voi_data.ROI,
    'Maximum': voi_max.Value,
    'Mean': voi_mean.Value,
    'Peak': voi_peak.Value
})

print(example)
