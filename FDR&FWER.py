import pandas as pd
import numpy as np
import statsmodels.stats.multitest as sm

uncorrected_p = [0.01, 0.019, 0.03, 0.045]
a = sm.multipletests(uncorrected_p, alpha=0.04, method='holm-sidak', is_sorted=False)

print(a)
