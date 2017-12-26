# -*- coding: cp936 -*-
import csv
import sys, os
import struct, datetime
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
import numpy as np

def read_csv(dirname, filename):
    #filename = "APD1��ѹ+5V_0.csv"
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


inpath = os.getcwd()##r"D:/Personal/Desktop/��������"
listmode = []
print os.getcwd()
##ttt = "D:/Personal/Desktop/��������/����QKDS-CCU���̲���_CCU״ָ̬ʾ1"
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
    print "�����ļ��У�", dirs, '      ', index, '  of  ', len(listdir)
    print "����ļ��У�", outdir
    print "�����С�����    ��ʼʱ��", datetime.datetime.now()
    if not os.path.exists(outdir):
        os.mkdir(outdir)
    for(dirname, dirshere, fileshere) in os.walk(dirs):
        for filename in fileshere:
            b = filename.find(r".csv")
            if (b >=0):
                ##print 'find'
                paracode, unit, listmode = read_csv(dirname, filename)
    
print "ȫ���������"


            
