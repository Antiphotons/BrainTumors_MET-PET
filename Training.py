import os.path
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

parameters = [[0.00001, 0.00001, 0.03278, 0.00003, 0.45510, 0.18604, 0.21214, 0.77499], 'huets']
parameters = [round(parameters[0][i], 5) for i in range(len(parameters[0]))]
print(parameters)
