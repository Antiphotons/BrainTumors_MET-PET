from matplotlib import pyplot as plt
import numpy as np

#some example data
x = np.linspace(0.1, 9.9, 20)
y = 3.0 * x
#some confidence interval
ci = 1.96 * np.std(y)/np.sqrt(len(x))

ax = plt.subplot()
ax.plot(x,y)
ax.fill_between(x, (y-ci), (y+ci), color='g')

plt.savefig('ex.png')