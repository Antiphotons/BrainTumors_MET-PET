import pandas as pd

# VOI info load
voi_df = pd.read_csv('C:/Kotomin/Globalall/Methionine_dyn/02_TAC/VOI_TACs/SkrynnikovVA_all.csv', sep=',')
# delete CT information and last strings
voi_df = voi_df[voi_df.Volume != 'CT - CT 3.27 mm']
voi_df = voi_df[voi_df.ROI != 'PERCIST 1.0']


# function of VOI choosing
def voi_choose(dataframe, voi):
    df = dataframe[dataframe.ROI == voi]
    return df


# generating the list of VOI
voi_list = pd.Series(voi_df['ROI']).unique()

# Particular VOI dataframes generation
for i in range(len(voi_list)):
    voi_df_nw = voi_choose(voi_df, voi_list[i])

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

    voi_name = voi_list[i]
    print(voi_name)
    #voi_df_nw.to_csv(voi_name, sep='\t')
