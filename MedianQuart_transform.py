import pandas as pd

# file read
path = 'G:/Kotomin-RABOTA/Globalall/Methionine_dyn/ПНИ/'
file = 'medians.csv'
tbl = pd.read_csv(path + file, sep=';', dtype={'Median': str,
                                                'Lower': str, 'Upper': str})

tbl.MedQuart = tbl['Median'] + ' (' + tbl['Lower'] + '–' + tbl['Upper'] + ')'
print(tbl.MedQuart)
tbl.MedQuart.to_csv('MedQuart.csv', sep='\t')
