# -*- coding:cp936 -*-
import os
import csv
import ftplib
import socket
from datetime import date, timedelta

HOST = '192.168.2.101'
USER = 'QKDS'
PASSWORD = 'QKDS'
DRROOT = '/TG02/PRODUCTS/QKDS/'

DRIN = '/TG02/PRODUCTS/QKDS/ENG_PRO/LEVEL0C/'
DRLIST = ['ATP', 'CCU', 'PPD', 'PRD1', 'PRD2']

DRIN2 = '/TG02/PRODUCTS/QKDS/TTC_PRO/LEVEL0C/'
DRLIST2 = ['DTD']

DRDATA = '/TG02/PRODUCTS/QKDS/SCI_PRO/LEVEL0B/'
DRLIST3 = ['GZD', 'IMG', 'LZTX', 'MYYY', 'XXX']

delta_day = 3  # 获取多少天的数据
offset_day = 0
start_day = 0  ##与offset_day配合实现获取哪一天开始的数据
delta_stop = offset_day + start_day
delta_start = delta_stop + delta_day
start_time = "20" + (date.today() - timedelta(days=delta_start)).strftime("%y%m%d") + "120000"
stop_time = "20" + (date.today() - timedelta(days=delta_stop)).strftime("%y%m%d") + "120000"


def match_file(files_in, start_time, stop_time, matchcsv):
    files_in.sort()
    files_in.reverse()
    ##对文件列表从后往前搜索，速度会更快，这是基于查询的都是最近的数据
    matched_files = []
    stop_idx = 0
    start_idx = 0
    find_start = 0
    find_stop = 0
    real_start = ""
    real_stop = files_in[0].split('_')[-3]
    for ss in files_in:
        strs = ss.split('_')
        file_start = strs[-4]
        file_stop = strs[-3]
        if (file_start < start_time and file_stop > start_time and find_start == 0):
            start_idx = files_in.index(ss)
            real_start = file_start
            find_start = 1
            break

        if (file_start < stop_time and file_stop > stop_time):
            stop_idx = files_in.index(ss)
            real_stop = file_stop
            find_stop = 1
    if (start_idx == stop_idx):
        matched_files.append(files_in[start_idx])
    else:
        matched_files = files_in[stop_idx:start_idx]
    matched_files.reverse()
    print
    stop_idx, start_idx, find_start, find_stop
    return real_start, real_stop, matched_files


def login_ftp():
    try:
        ftp = ftplib.FTP(HOST)
    except (socket.error, socket.gaierror):
        print('ERROR: cannot reach "%s"' % HOST)
        return
    print('****** connect to host "%s"' % HOST)

    try:
        ftp.login(USER, PASSWORD, 8080)
    except:
        print('ERROR: login failed with "%s" and "%s"' % USER, PASSWORD)
        ftp.quit()
        return
    print('*** login success')
    return ftp, True


##登录FTP
##ftp, state = login_ftp()

##生成访问目录列表
print("get file")
print("get date")

print("start time", start_time, "stop time", stop_time)

##筛选并获取数据
targetfile_list = []
raw_dir = os.getcwd() + "/raw_data/"
merge_dir = os.getcwd() + "/merge_data/"
if (not os.path.exists(raw_dir)):
    os.makedirs(raw_dir)
print(raw_dir)
dirlist = ['CCU']

# for ss in DRLIST:
# dirlist.append(DRIN+ss+'/')
# for ss in DRLIST2:
# dirlist.append(DRIN2+ss+'/')

##合并文件
tmp_merge = merge_dir + start_time + '-' + stop_time + '/'
merged_files = []
print("merged data directory:", tmp_merge)
if (not os.path.exists(tmp_merge)):
    os.makedirs(tmp_merge)

for ss in dirlist:
    tmp_dir = raw_dir + ss

    print('raw data directory:', tmp_dir)
    if (not os.path.exists(tmp_dir)):
        os.makedirs(tmp_dir)

    files_in = os.listdir(tmp_dir)
    print(files_in)
real_start, real_stop, matched_files = match_file(files_in, start_time, stop_time, 1)
print("real start time", real_start, "real stop time", real_stop)

merged_filename = matched_files[-1][:matched_files[-1].index("_2")] + '_' + real_start + '-' + real_stop + '.csv'
print("merged file name:", merged_filename)
start = 1
writer = csv.writer(open(os.path.join(tmp_merge, merged_filename), 'w'), delimiter=',', lineterminator='\n')
for s_file in matched_files:
    print('files to be merged:', s_file)
    reader = csv.reader(open(s_file, 'r'), delimiter=',')
    if (start == 0):
        data = reader.next()
    else:
        start = 0
    for row in reader:
        writer.writerow(row)
merged_files.append(merged_filename)
##+'\\'+matched_files[-1][:matched_files[-1].index("_2")]

##对合并后的每一个文件的每一列数据绘图
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig


def print_csv(x_list, unit, listv, listv1, dirname, filename, outdir):
    mode = (u'待机', u'分发', u'', u'接收', u'提取', u'激光', u'')
    y_pos = np.arange(len(mode))
    x_pos = np.arange(len(x_list))
    fig, host = plt.subplots()

    par1 = host.twinx()
    p1, = host.plot(range(0, len(listv)), listv, 'b-', label=u'物理值')
    p2, = par1.plot(range(0, len(listv1)), listv1, 'r-', label=u'工作模式')

    host.set_xlim(0, len(listv))
    if (filename.find('温度') > -1):
        if (filename.find('APD') > -1):
            host.set_ylim(-17, (max(listv) + 0.1) * 1.1)
        else:
            host.set_ylim(10, (max(listv) + 0.1) * 1.1)
    else:
        host.set_ylim((min(listv) - 0.1) * 0.9, (max(listv) + 0.1) * 1.1)

    plt.yticks(y_pos, mode, rotation=0)

    nn = x_pos[::int(len(x_list) / 4)]
    xx = []
    for ii in nn:
        xx.append(x_list[ii][2:16])
    plt.xticks(nn, xx, rotation=15)

    host.set_xlabel(u'采样点')
    host.set_ylabel(u'单位：' + unit)
    par1.set_ylabel(u'模式')

    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())

    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1, p2]
    host.legend(lines, [l.get_label() for l in lines])
    ss = filename.decode('cp936')

    plt.title(ss[:ss.find('-')])
    if (filename.find('/') > 0):
        tt = filename.split('/')  # [filename.index('/')]='_'
        filename = tt[0] + tt[1]
    filename = filename.strip() + '.png'
    # print filename
    pathname = os.path.join(outdir, filename)

    savefig(pathname)
    plt.clf()
    plt.close()


for ff in merged_files:
    print("绘图文件:" + ff)
    reader = csv.reader(open(tmp_merge + ff, 'r'), delimiter=',', lineterminator='\n')
    header = reader.next()
    data_array = []
    head_list = []
    colums = len(header)
    j = 0
    for row in reader:
        if (len(row) < colums):
            continue
        head_list.append(row[0])
        for i in range(1, colums):
            if (row[i].find('0x') > -1):
                data_array.append(float(eval(row[i])))
            else:
                try:
                    aa = float(row[i])
                except:
                    aa = 0
                data_array.append(aa)
    for i in range(1, colums):
        listv = data_array[i - 1::colums - 1]
        listmode = []
        # print listv
        print_csv(head_list, "", listv, listmode, tmp_merge, header[i] + '-' + real_start + '-' + real_stop, tmp_merge)
