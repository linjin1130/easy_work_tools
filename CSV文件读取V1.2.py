# -*- coding: cp936 -*-
import matplotlib.pyplot as plt; plt.rcdefaults()
import numpy as np
import matplotlib.pyplot as plt


# Example data
mode = (u'待机', u'分发', u'接收', u'提取', u'激光')
y_pos = np.arange(len(mode))
performance = 3 + 10 * np.random.rand(len(mode))
error = np.random.rand(len(mode))

plt.barh(y_pos, performance, xerr=error, align='center', alpha=0.4)
plt.yticks(y_pos, mode)
plt.xlabel('Performance')
plt.title('How fast do you want to go today?')
plt.show()
