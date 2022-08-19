import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

parameters = ['tits', 'dicks']
x = pd.DataFrame(
    {
        'big': ['', ''],
        'small': ['', '']
    },
    index=parameters,
)
x.index.name = 'Parameter'

dwarf, elf = x, x

dwarf['big'].loc['tits'] = 6
elf['big'].loc['tits'] = 2
print(dwarf)
print()
print(elf)
print()
print(x)
