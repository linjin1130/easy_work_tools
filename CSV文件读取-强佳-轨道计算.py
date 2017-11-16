# -*- coding: cp936 -*-
import csv
import sys, os
import struct, datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import numpy as np

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


inpath = os.getcwd()##r"D:/Personal/Desktop/导出数据"
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
        for filename in fileshere:
            b = filename.find(r".csv")
            if (b >=0):
                ##print 'find'
                paracode, unit, listmode = read_csv(dirname, filename)
    
print "全部处理结束"


            
