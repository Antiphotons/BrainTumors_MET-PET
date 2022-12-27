import pandas as pd
import numpy as np
import statsmodels.stats.multitest as sm

# path to csv-file with data
folder = 'C:/Kotomin/Globalall/Methionine_dyn/01_Intervals/csv/'
file = 'uncorrected_p.csv'

# df load & empty rows deletion
uncorr_p = pd.read_csv(folder + file, sep='\t', dtype={'uncorrected_p': np.float64})
uncorr_p = uncorr_p['uncorrected_p'].tolist()

#print(uncorr_p)

example_p = [0.00001, 0.00001, 0.03278, 0.00003, 0.45510, 0.18604, 0.21214, 0.77499]
corr_p = sm.multipletests(example_p, alpha=0.05, method='holm-sidak', is_sorted=False)
print(corr_p)

corr_p = sm.multipletests(uncorr_p, alpha=0.05, method='holm-sidak', is_sorted=False)
rounded_corr_p = [round(corr_p[1][i], 4) for i in range(len(corr_p[1]))]
#print(rounded_corr_p)

# corr_p_int = pd.Series(rounded_corr_p)
# corr_p_int.to_csv('corr_p_int.csv', sep='\t')

#corr_p_par = pd.Series(rounded_corr_p)
#corr_p_par.to_csv('corr_p_par.csv', sep='\t')
