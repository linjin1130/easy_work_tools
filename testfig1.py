# # -*- coding: cp936 -*-
# import matplotlib.pyplot as plt
#
# plt.xlabel('�Ա�')
# plt.ylabel('����')
# plt.title('�Ա��������')
# plt.xticks ((0,1),('��','Ů'))
# rect = plt.bar(left = (0,1),height = (1,0.5), width = 0.35, align="center", yerr=0.000001)
#
# plt.legend((rect,),("ͼ��",))
#
# plt.show()
"""
Demo of custom property-cycle settings to control colors and such
for multi-line plots.

This example demonstrates two different APIs:

    1. Setting the default rc-parameter specifying the property cycle.
       This affects all subsequent axes (but not axes already created).
    2. Setting the property cycle for a specific axes. This only
       affects a single axes.
"""
from cycler import cycler
import numpy as np
import matplotlib.pyplot as plt

x = np.linspace(0, 2 * np.pi)
offsets = np.linspace(0, 2*np.pi, 4, endpoint=False)
# Create array with shifted-sine curve along each column
yy = np.transpose([np.sin(x + phi) for phi in offsets])

plt.rc('lines', linewidth=4)
plt.rc('axes', prop_cycle=(cycler('color', ['r', 'g', 'b', 'y']) +
                           cycler('linestyle', ['-', '--', ':', '-.'])))
fig, ax0 = plt.subplots(nrows=1)
print(yy)
ax0.plot(yy)
ax0.set_title('Set default color cycle to rgby')

# Tweak spacing between subplots to prevent labels from overlapping
plt.subplots_adjust(hspace=0.3)
plt.show()
