# -*- coding: cp936 -*-
import csv

with open(u"D:/Personal/Desktop/导出数据/量子QKDS-量子单元工程参数1_APD1电压+5V/APD1电压+5V_0.csv", 'r') as csvfile:
    spamreader = csv.reader(csvfile, delimiter=',')
    paracode, meaning, unit, rawcode, segcode, phyvalue = spamreader.next()
    print paracode, meaning, unit, rawcode, segcode, phyvalue
    for paracode, meaning, unit, rawcode, segcode, phyvalue in spamreader:
        pass##print phyvalue
    
import matplotlib.pyplot as plt

def make_patch_spines_invisible(ax):
    ax.set_frame_on(True)
    ax.patch.set_visible(False)
    for sp in ax.spines.itervalues():
        pass##sp.set_visible(False)

fig, host = plt.subplots()##Create a figure with a set of subplots already made.
##This utility wrapper makes it convenient to create common layouts of
##subplots, including the enclosing figure object, in a single call.
fig.subplots_adjust(right=0.75)##Tune the subplot layout.fig的subplots的右边位置

par1 = host.twinx()
par2 = host.twinx()
##Make a second axes that shares the *x*-axis.  The new axes will
##overlay *ax* (or the current axes if *ax* is *None*).  The ticks
##for *ax2* will be placed on the right, and the *ax2* instance is
##returned.

# Offset the right spine of par2.  The ticks and label have already been
# placed on the right by twinx above.
par2.spines["right"].set_position(("axes", 1.2))##向右调整par2的右纵轴
##spines an axis spine -- the line noting the data area boundaries
 
##Spines are the lines connecting the axis tick marks and noting the
##boundaries of the data area. They can be placed at arbitrary
##positions. See function:`~matplotlib.spines.Spine.set_position`
##for more information.
## 
##The default position is ``('outward',0)``.
## 
##Spines are subclasses of class:`~matplotlib.patches.Patch`, and
##inherit much of their behavior.
## 
##Spines draw a line or a circle, depending if
##function:`~matplotlib.spines.Spine.set_patch_line` or
##function:`~matplotlib.spines.Spine.set_patch_circle` has been
##called. Line-like is the default.
# Having been created by twinx, par2 has its frame off, so the line of its
# detached spine is invisible.  First, activate the frame but make the patch
# and spines invisible.
make_patch_spines_invisible(par2)##让par2不可见
# Second, show the right spine.
#par2.spines["right"].set_visible(True)##仅显示右轴

p1, = host.plot([0, 1, 2], [0, 1, 2], "b-", label="Density")
p2, = par1.plot([0, 1, 2], [0, 3, 2], "r-", label="Temperature")
p3, = par2.plot([0, 1, 2], [50, 30, 15], "g-", label="Velocity")

##设置各轴的轴坐标范围
host.set_xlim(0, 2)
host.set_ylim(0, 2)
par1.set_ylim(0, 4)
par2.set_ylim(1, 20)

##设置各轴的轴标签
host.set_xlabel("Distance")
host.set_ylabel("Density")
par1.set_ylabel("Temperature")
par2.set_ylabel("Velocity")

##设置各轴的轴标签的颜色
host.yaxis.label.set_color(p1.get_color())
par1.yaxis.label.set_color(p2.get_color())
par2.yaxis.label.set_color(p3.get_color())

##设置各轴的线宽与颜色
tkw = dict(size=4, width=1.5)
host.tick_params(axis='y', colors=p1.get_color(), **tkw)
par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
host.tick_params(axis='x', **tkw)

lines = [p1, p2, p3]
##设置图例
host.legend(lines, [l.get_label() for l in lines])

plt.show()
