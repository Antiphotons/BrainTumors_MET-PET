# print(voi_df.iloc[1]) example of indexation

import pandas as pd

voi = pd.Series([1, 30, 4, 10])
v = 'voi.csv'
voi.to_csv(v, sep='\t')