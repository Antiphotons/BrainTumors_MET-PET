import os.path
import random
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import math as m
tac = pd.DataFrame({
    'Mean': [0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 188, 210,
                           225, 240, 255, 270, 285, 300, 315, 330, 345, 360, 375, 390, 405, 420,
                           435, 450, 465, 480, 495, 510, 525, 540, 555, 570, 585, 600, 630, 660,
                           690, 720, 750, 780, 810, 840, 870, 900, 930, 960, 990, 1020, 1050, 1080,
                           1110, 1140, 1170, 1200, 1320, 1440, 1560, 1680, 1800, 1920, 2040, 2160, 900]
})
times = pd.Series([0, 15, 30, 45, 60, 75, 90, 105, 120, 135, 150, 165, 180, 195, 210,
                           225, 240, 255, 270, 285, 300, 315, 330, 345, 360, 375, 390, 405, 420,
                           435, 450, 465, 480, 495, 510, 525, 540, 555, 570, 585, 600, 630, 660,
                           690, 720, 750, 780, 810, 840, 870, 900, 930, 960, 990, 1020, 1050, 1080,
                           1110, 1140, 1170, 1200, 1320, 1440, 1560, 1680, 1800, 1920, 2040, 2160, 2280])

tac_mean = pd.Series([(m.log(t + 1) - (t + 1) ** (0.3)) ** 2 for t in tac['Mean'].tolist()])
tac['Mean'], tac['Time'] = tac_mean, times

for i in range(0, 10):
    tac.loc[i, 'Mean'] = sum(tac.Mean.loc[i:i + 1]) / 2
    tac.drop(tac.index[i + 1], inplace=True)
    tac = tac.reset_index()
    del tac['index']

for i in range(10, 15):
    tac.loc[i, 'Mean'] = sum(tac.Mean.loc[i:i + 3]) / 4
    tac.drop(tac.index[i + 3], inplace=True)
    tac.drop(tac.index[i + 2], inplace=True)
    tac.drop(tac.index[i + 1], inplace=True)
    tac = tac.reset_index()
    del tac['index']

for i in range(15, 20):
    tac.loc[i, 'Mean'] = sum(tac.Mean.loc[i:i + 3]) / 4
    tac.drop(tac.index[i + 3], inplace=True)
    tac.drop(tac.index[i + 2], inplace=True)
    tac.drop(tac.index[i + 1], inplace=True)
    tac = tac.reset_index()
    del tac['index']

plt.plot(tac.Time.tolist(), tac.Mean.tolist())
plt.savefig('smooth.png')

print(tac)
