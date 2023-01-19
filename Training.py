#import os.path
import pandas as pd
#from math import inf
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.stats import levene
#from statistics import mean, stdev
#import seaborn as sns


df = pd.DataFrame({
    'a': ['siski', 'kiski', 'diski'],
    'b': ['piski', 'na viske', 'po-angliyski']
})

df['ab'] = df.a + '-' + df.b
print(df['ab'].unique())


d = {
    'a': ['siski', 'kiski', 'diski'],
    'b': ['piski', 'na viske', 'po-angliyski']
}

print(d['a'])