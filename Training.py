import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import levene

params = ['a', 'b', 'c', '1-1', '2-2', '3-3', 'd', 'e', 'f']
resids = ['1-1', '2-2', '3-3']
new_params = [params[i] for i in range(len(params)) if i % 6 < 3]

var_df = pd.DataFrame(data=None, index=params, columns=resids)
var_df['2-2']['c'] = 'dfjng'
print(new_params)
