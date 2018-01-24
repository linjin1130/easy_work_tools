##画出李萨育图形

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
fig = plt.figure(dpi=100)
ax = Axes3D(fig)

t = np.arange(0, 10, 0.001)
x = np.cos(2*np.pi*t)
plt.subplot(2,1,1)
plt.plot(x, t, 0*t)
y = np.sin(2 * np.pi * f * t)

plt.subplot(1, 5, f)
plt.plot(x, y, color=colors[f-1])

ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap='rainbow')

plt.savefig('李萨育图形.jpg')