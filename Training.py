import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import levene

params = ['a', 'b', 'c']
resids = ['1-1', '2-2', '3-3']

var_df = pd.DataFrame(data=None, index=params, columns=resids)
var_df['2-2']['c'] = 'dfjng'
print(var_df)
