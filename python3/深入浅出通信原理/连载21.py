##画出李萨育图形

import numpy as np
import matplotlib.pyplot as plt
colors = ['r', 'g', 'b', 'y', 'c', 'm', 'k']
plt.figure(figsize=(25,5), dpi=100)
for f in range(1,6):
    t = np.arange(0, 1000, 0.001)
    x = np.cos(2*np.pi*t)
    y = np.sin(2 * np.pi * f * t)

    plt.subplot(1, 5, f)
    plt.plot(x, y, color=colors[f-1])
    plt.axis('off')
plt.savefig('李萨育图形.jpg')