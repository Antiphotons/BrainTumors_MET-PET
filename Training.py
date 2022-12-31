#import os.path
#import pandas as pd
#import matplotlib.pyplot as plt
#import numpy as np
#from scipy.stats import levene
#from statistics import mean, stdev
#import seaborn as sns

option = 'params'

dict = {'df': 0, 'params': 1, 'resids': 2}
dict2 = [111, 222, 333]
print(dict2[dict.get(option)])
