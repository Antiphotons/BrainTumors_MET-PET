import os.path
import random
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import math as m


df = pd.DataFrame([
	[-10, -9, 8],
	[6, 2, -4],
	[-8, 5, 1]],
	columns=['a', 'b', 'c'])

df.loc[(df.a < 0), 'a'] = 0
print(df)

