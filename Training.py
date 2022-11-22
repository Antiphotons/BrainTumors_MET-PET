import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import levene

df = pd.DataFrame({
    '1': [1, 5, 9, 13, 17],
    '2': [1, 3, 5, 7, 9]
})

var1 = np.var(df['1'])
var2 = np.var(df['2'])
lev = levene(df['1'], df['2'], center='median')

print(df)
print(var1, var2)
print(lev)
