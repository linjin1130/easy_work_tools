import numpy as np
import matplotlib.pyplot as plt
x = np.arange(-8, 8, 0.01)
# plt.plot(x, np.sinc(x))
# plt.show()

y = np.arange(-8, 8, 1)
mk, stem, baseline = plt.stem(y, np.sinc(y/2), '-.')
plt.setp(baseline, 'color', 'b', 'linewidth', 2)
plt.grid()
plt.show()