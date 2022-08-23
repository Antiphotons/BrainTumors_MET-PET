import pandas as pd
import numpy as np
import statsmodels.stats.multitest as sm

all_p = [0.00001, 0.00001, 0.03278, 0.00003, 0.45510, 0.18604, 0.21214, 0.77499]
benign_p = [0.00620, 0.04979, 0.74082, 0.36788, 0.83176, 0.45943, 0.60653, 0.49659]
malignant_p = [0.00001, 0.00547, 0.55873, 0.02765, 0.89159, 0.58895, 0.29309, 0.66248]

all = sm.multipletests(all_p, alpha=0.05, method='holm-sidak', is_sorted=False)
benign = sm.multipletests(benign_p, alpha=0.05, method='holm-sidak', is_sorted=False)
malignant = sm.multipletests(malignant_p, alpha=0.05, method='holm-sidak', is_sorted=False)
all_corr_p = [round(all[1][i], 4) for i in range(len(all[1]))]
benign_corr_p = [round(benign[1][i], 4) for i in range(len(benign[1]))]
malignant_corr_p = [round(malignant[1][i], 4) for i in range(len(malignant[1]))]
print(all_corr_p)
print()
print(benign_corr_p)
print()
print(malignant_corr_p)
