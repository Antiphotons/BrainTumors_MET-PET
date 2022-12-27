import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from scipy.stats import levene

df = pd.DataFrame({
    '1': [1, 5, 9, 13, 17],
    '2': [1, 3, 5, 7, 9]
})
df.loc[len(df.index)] = [99, 99]
print(df)
