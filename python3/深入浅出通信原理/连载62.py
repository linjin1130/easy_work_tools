import numpy as np
import matplotlib.pyplot as plt

def square(x, duty):
    y = []
    for i in x:
        if np.sin(i) > np.sin(1/2):  # 调用sin，cos要使用np.sin，np.cos
            y.append(1)
        else:
            y.append(-1)
    return np.array(y)

x = np.arange(-8, 8, 0.01)
# plt.plot(x, 0.5+0.5*square(np.pi*x+0.5*np.pi, 50))

xt = np.arange(-16, 16, 1)
markerline, stemline, baseline = plt.stem(xt, np.sinc(0.25*xt), '-')
# plt.setp(baseline, 'color', 'y', 'linewidth', 4)
plt.show()