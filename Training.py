import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import levene
from statistics import mean, stdev

df = pd.DataFrame({
    '0':[1, 2, 3, 4, 5, 6, 7, 8, 9],
#    '1': [1, 5, 9, 13, 17],
#    '2': [1, 3, 5, 7, 9]
})

bs_means = []
bs_sds = []
for _ in range(1000):
    x = np.random.choice(df['0'], size=9, replace=True)
    bs_means.append(mean(x))
    bs_sds.append(stdev(x))

print(mean(df['0']), stdev(df['0']))
print(mean(bs_means), np.percentile(bs_means, 2.5), '–', np.percentile(bs_means, 97.5))
print (mean(bs_sds), np.percentile(bs_sds, 2.5), '–', np.percentile(bs_sds, 97.5))
