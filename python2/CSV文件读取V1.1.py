# -*- coding: cp936 -*-
import csv
import sys, os
import struct

def read_csv(dirname, filename):
    #filename = "APD1电压+5V_0.csv"
    #filename = filename[:filename.find("_0.csv")]
    #print filename
    ipathname = os.path.join(dirname, filename)
    unit = ""
    with open(ipathname, 'r') as csvfile:
        spamreader = csv.reader(csvfile, delimiter=',')
        paracode0, meaning0, unit0, rawcode0, segcode0, phyvalue0 = spamreader.next()
        ##print paracode, meaning, unit, rawcode, segcode, phyvalue
        listv = []
        for paracode, meaning, unit, rawcode, segcode, phyvalue in spamreader:
            if phyvalue.find('x')>0:
                phyvalue = phyvalue[phyvalue.index('x')+1:]
            listv.append(float(phyvalue))##print phyvalue
    return paracode, unit, listv

import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import numpy as np

def print_csv(paracode, unit, listv, listv1, dirname, filename, outdir):
    mode = (u'待机', u'分发', u'', u'接收', u'提取', u'激光', u'',)
    y_pos = np.arange(len(mode))

    fig, host = plt.subplots()
    ##Create a figure with a set of subplots already made.
    ##This utility wrapper makes it convenient to create common layouts of
    ##subplots, including the enclosing figure object, in a single call.
    ##fig.subplots_adjust(right=0.75)##Tune the subplot layout.fig的subplots的右边位置，即让右边多留0.75的位置出来

    par1 = host.twinx()
    p1, = host.plot(range(0,len(listv)), listv, "b-", label="物理值")
    p2, = par1.plot(range(0,len(listv1)), listv1, "r-", label="工作模式")
    #p3, = par2.plot([0, 1, 2], [50, 30, 15], "g-", label="Velocity")

    ##设置各轴的轴坐标范围
    host.set_xlim(0, len(listv))
    if(unit.find('℃')>=0):
        if(filename.find('APD')>=0):
            host.set_ylim(12, (max(listv)+0.1)*1.2)
        else:
            host.set_ylim(-17, (max(listv)+0.1)*1.2)
    else:
        host.set_ylim((min(listv)-0.1)*0.8, (max(listv)+0.1)*1.2)
    ##print (min(listv)-0.1), (max(listv)+0.1)
    plt.yticks(y_pos, mode)
    #par1.set_ylim(0, 4)
    #par2.set_ylim(1, 20)

    ##设置各轴的轴标签
    host.set_xlabel("采样点")
    host.set_ylabel("单位（"+unit+"）")
    par1.set_ylabel("模式")
    #par2.set_ylabel("Velocity")

    ##设置各轴的轴标签的颜色
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    #par2.yaxis.label.set_color(p3.get_color())

    ##设置各轴的线宽与颜色
    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    #par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    #lines = [p1, p2, p3]
    lines = [p1,p2]
    ##设置图例
    host.legend(lines, [l.get_label() for l in lines])

    plt.title(paracode+filename)
    ttt = ""
    sStr2 = r"\/"
    for c in paracode:
        if c in sStr2:
            ttt = ttt+'_'
        else:
            ttt = ttt+c
    filename = ttt+'_'+filename[:filename.find(".csv")-2]+'.png'
    pathname = os.path.join(outdir,filename)
    savefig(pathname)
    plt.clf()
    plt.close()

import sys, os
import struct, datetime
inpath = r"D:/Personal/Desktop/导出数据"
listmode = []
print os.getcwd()
##ttt = "D:/Personal/Desktop/导出数据/量子QKDS-CCU工程参数_CCU状态指示1"
##print type(ttt)
listdir = []
index = 0
piccount = 0
for files in os.listdir(inpath):
    newf = os.path.join(inpath,files)
    if os.path.isdir(newf):
        listdir.append(newf)
for dirs in listdir:
    index += 1
    outdir = os.path.join(dirs,"output")
    print "处理文件夹：", dirs, '      ', index, '  of  ', len(listdir)
    print "输出文件夹：", outdir
    print "处理中。。。    开始时间", datetime.datetime.now()
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for(dirname, dirshere, fileshere) in os.walk(dirs):
        a = dirname.find("CCU状态指示1")
        for filename in fileshere:
            b = filename.find(r"工作模式_0.csv")
            if (a>=0 and b >=0):
                ##print 'find'
                paracode, unit, listmode = read_csv(dirname, filename)
    
    for(dirname, dirshere, fileshere) in os.walk(inpath):
        for filename in fileshere:
            if filename.endswith(".csv")>0 and dirname.find("CCU状态指示1")<0 and filename.find("工作模式_0.csv")<0:
                paracode, unit, listv = read_csv(dirname, filename)
                print_csv(paracode, unit, listv, listmode, dirname, filename, outdir)
                piccount += 1
    print "处理结束。。。  结束时间", datetime.datetime.now(), "输出图片", piccount, "张"
print "全部处理结束"


            
