import pandas as pd
voi = pd.DataFrame({
    'pluses': [1, 2, 5, 8, 0],
    'minuses': [-1, -2, -5, -8, 0]
})

voi_trnspz = pd.Series.transpose(voi['pluses'])
print(voi_trnspz)
