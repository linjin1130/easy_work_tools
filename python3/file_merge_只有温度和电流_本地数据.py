# -*- coding:cp936 -*- 
import os
import csv
import ftplib
import socket
from datetime import date,timedelta,datetime
# import datetime
import time

# start_day = 20170301
# stop_day = 20170331
# start_time = str(start_day)+"120000"
# stop_time  = str(stop_day)+"120000"

DRLIST = ['CCU_','ATP_', 'PRD1','PRD2','DTD_']#'PPD_',
ST_name = ['模式','量子通信','QKD','ATP','EDFA','信标光','LD1','LD2','LD3','LD4']#统计参数名字
ST_COL  = [21,22,15,17,18,41,25,25,25,25]# 其所在列数
col_bit = [8,2,16,16,16,16,0,1,2,3]#所在列数的参数的bit位 =16表示浮点数， =8表示取模式位的低3位
pre_list = [0 for i in range(len(ST_name))]
cur_list = [0 for i in range(len(ST_name))]
evnt_list = [[] for i in range(len(ST_name))]
#需要统计的信息
#1. 量子通信次数&总时长
#2. QKD加电次数&总时长
#3. ATP加电次数&总时长
#4. EDFA加电次数&总时间
#5. 信标光加电次数&总时间
#6. 分发模式次数、激光通信模式次数
#7. 各LD开启次数&加电时间

PDHU = ['PDHU',]

temper_name = [u'次镜本体温度',u'主镜本体温度',u'光学主体框架温度',u'第一折转镜温度',u'U型架（电机侧）温度',u'U型架（旋变侧）温度',u'方位轴系基座温度',u'后光路温度',u'LD（主）温度',u'次镜盖温度',u'信标光主体温度',u'粗跟踪温度',u'方位轴温度',u'LD（备）温度',u'EDFA温度',u'量子接收模块温度']

delta_day = 2#获取多少天的数据
offset_day = 0
start_day = 0 ##与offset_day配合实现获取哪一天开始的数据
delta_stop = offset_day+start_day
delta_start = delta_stop+delta_day

start_time = "20"+(date.today()-timedelta(days=delta_start)).strftime("%y%m%d")+"120000"
stop_time  = "20"+(date.today()-timedelta(days=delta_stop)).strftime("%y%m%d")+"120000"
start_time = "20180101120000"
stop_time  = "20180412120000"
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
    real_stop = files_in[0].split('_')[-2]
    for ss in files_in:
        strs = ss.split('_')
        file_start = strs[-3]
        file_stop = strs[-2]
        if(file_start > start_time):
            start_idx = files_in.index(ss)+1
            real_start = file_start
            find_start = 1
        if(file_stop < start_time):
            break

            
        if(file_start < stop_time and find_stop == 0):
            stop_idx = files_in.index(ss)
            real_stop = file_stop
            find_stop = 1

    if(start_idx == stop_idx):
        matched_files.append(files_in[start_idx])
    else:
        matched_files = files_in[stop_idx:start_idx]
    matched_files.reverse()
    print(stop_idx, start_idx, find_start, find_stop)
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

##生成访问目录列表
print("get file")
print("get date")

print("start time", start_time, "stop time", stop_time)

##筛选并获取数据
targetfile_list = []
data_path = "E:/工程相关/9XX/9XX数据"
raw_dir = data_path+"/raw_data/"
merge_dir = data_path+"/merge_data/"
if(not os.path.exists(raw_dir)):
    os.makedirs(raw_dir)
print(raw_dir)
######################
dirlist = []

##合并文件
tmp_merge = merge_dir+start_time+'-'+stop_time+'/'
merged_files = []

for ss in DRLIST:
    dirlist.append(raw_dir+ss+'/')

print("merged data directory:",tmp_merge)
if(not os.path.exists(tmp_merge)):
    os.makedirs(tmp_merge)

#将文件分类放入各自的文件中
import shutil
files_in = os.listdir(raw_dir)

for ff in files_in:
    #print(ff,os.path.isfile(ff))
    if(ff.find('T2_QKDS_')>-1):
        folder_name = ff[8:12]
        #print(folder_name)
        tmp_fold = os.path.join(raw_dir, folder_name)
        if not os.path.exists(tmp_fold):
            os.mkdir(tmp_fold)
        shutil.move(os.path.join(raw_dir, ff), os.path.join(tmp_fold, ff))

for ss in dirlist:
    tmp_dir = raw_dir + ss[ss.rfind('0C') + 3:]

    print('raw data directory:', tmp_dir)
    if (not os.path.exists(tmp_dir)):
        os.makedirs(tmp_dir)

    files_in = os.listdir(ss)
    real_start, real_stop, matched_files = match_file(files_in, start_time, stop_time, 1)
    print("real start time", real_start, "real stop time", real_stop)
    downloaded_files = matched_files
    print(downloaded_files)
    merged_filename = matched_files[-1][:matched_files[-1].index("_2")] + '_' + real_start + '-' + real_stop + '.csv'
    print("merged file name:", merged_filename)
    if (not os.path.exists(os.path.join(tmp_merge, merged_filename))) or (merged_filename.find('DTD')>0):
        start = 1
        print(ss)
        print(time.time())
        writer = csv.writer(open(os.path.join(tmp_merge, merged_filename), 'w'), delimiter=',', lineterminator='\n')
        factor = delta_day
        is_DTD = 0
        if downloaded_files[0].find('DTD') > 0:
            factor = delta_day * 4
            is_DTD = 1
        for s_file in downloaded_files:
            #print('files to be merged:', s_file)
            reader = csv.reader(open(os.path.join(ss,s_file), 'r'), delimiter=',')
            if (start == 0):
                data = reader.__next__()
            else:
                start = 0
            for ii,row in enumerate(reader):
                if((ii%factor)==0):
                    writer.writerow(row)


    merged_files.append(merged_filename)
    print(time.time())
    ##+'\\'+matched_files[-1][:matched_files[-1].index("_2")]

    # ta = datetime.strptime(tt[0][0], "%Y-%m-%d %H:%M:%S")
    # tb = datetime.strptime(tt[1][0], "%Y-%m-%d %H:%M:%S")
    # print(tb,ta)
    # dlt = tb-ta
    #print(dlt)
    #for t, v in tt:
        # ta = time.strptime(t, "%Y-%m-%d %H:%M:%S")
        # print(ta)
    #print(tt)
#需要统计的信息
#1. 量子通信次数&总时长
#2. QKD加电时长
#3. ATP加电时长
#4. EDFA加电时间
#5. 信标光加电时间
#6. 分发模式次数、激光通信模式次数
#7. 各LD开启次数&加电时间

print(time.time())
dirlist = []
dirlist.append(raw_dir+PDHU[0])
for ss in dirlist:
    if not os.path.exists(ss):
        break
    ##1. 生成并创建本地存放目录
    tmp_dir = raw_dir + 'PDHU' + ss[ss.rfind('0C') + 3:]
    print('raw data directory:', tmp_dir)
    if (not os.path.exists(tmp_dir)):
        os.makedirs(tmp_dir)
    ##3 获取该目录下存放的文件
    files_in = os.listdir(ss)

    ##4 根据条件筛选文件，并返回筛选出的文件目录
    real_start, real_stop, matched_files = match_file(files_in, start_time, stop_time, 1)
    # print(matched_files)
    print("real start time", real_start, "real stop time", real_stop)
    ##5 下载文件到本地
    downloaded_files = matched_files
    ##6 对下载的文件进行合并
    # print(downloaded_files)
    merged_filename = matched_files[-1][:matched_files[-1].index("_2")] + '_' + real_start + '-' + real_stop + '.csv'
    print("merged file name:", merged_filename)
    print(time.time())
    ##打开待写入文件
    writer = csv.writer(open(os.path.join(tmp_merge, merged_filename), 'w'), delimiter=',', lineterminator='\n')

    ##对第一个文件处理
    print(downloaded_files[0])
    head_file = downloaded_files[0]
    reader = csv.reader(open(os.path.join(ss,head_file), 'r'), delimiter=',')
    data = reader.__next__()
    # 对第一个文件，其第一行，找出需要提取的列
    col_idx = []
    col_idx.append(0)
    row_data = []
    row_data.append(data[0])
    for idx, col in enumerate(data):
        # print(col.find('量子'))
        if (col.find('量子') == True):
            # print(col.find('量子'))
            col_idx.append(idx)
            row_data.append(col)
            print(idx, '\n')
    ##将该文件剩下部分写入文件
    writer.writerow(row_data)
    print(col_idx)
    row_data = []
    for row in reader:
        row_data = [row[col_idx[0]], row[col_idx[1]], row[col_idx[2]], row[col_idx[3]], row[col_idx[4]],
                    row[col_idx[5]], row[col_idx[6]], row[col_idx[7]]]
        # for idx in range(len(col_idx)):
        #    row_data.append(row[col_idx[idx]])

        writer.writerow(row_data)
        # row_data = []
    ##将剩下的文件除第一行外部分写入文件
    for idx, s_file in enumerate(downloaded_files):
        print('files to be merged:', s_file)
        reader = csv.reader(open(s_file, 'r'), delimiter=',')
        data = reader.__next__()
        for row in reader:
            # for idx in range(len(col_idx)):
            #    try:
            #        row_data.append(row[col_idx[idx]])
            #    except:
            #        print(idx, col_idx[idx], len(row))
            #        print(row)
            try:
                row_data = [row[col_idx[0]], row[col_idx[1]], row[col_idx[2]], row[col_idx[3]], row[col_idx[4]],
                            row[col_idx[5]], row[col_idx[6]], row[col_idx[7]]]
            except:
                print(idx, len(row))
            writer.writerow(row_data)
            # row_data = []
    merged_files.append(merged_filename)
    ##+'\\'+matched_files[-1][:matched_files[-1].index("_2")]
print(time.time())
##对合并后的每一个文件的每一列数据绘图
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig


def print_csv(x_list, unit, listv, listv1, dirname, filename, outdir):
    mode = (u'待机', u'分发', u'', u'接收', u'提取', u'激光', u'')
    y_pos = np.arange(len(mode))
    x_pos = np.arange(len(x_list))
    plt.rc('figure', figsize=(18, 9))

    fig, host = plt.subplots()

    par1 = host.twinx()
    p1, = host.plot(range(0, len(listv)), listv, 'b-', label=u'物理值')
    # p3, = host.plot(range(0, len(listv)), listv, 'g-', label=u'物理值2')
    p2, = par1.plot(range(0, len(listv1)), listv1, 'r-', label=u'工作模式')

    host.set_xlim(0, len(listv))
    if (filename.find('温度') > -1):
        if (filename.find('APD') > -1):
            host.set_ylim(-17, (max(listv) + 0.1) * 1.1)
        else:
            host.set_ylim(5, (max(listv) + 0.1) * 1.1)
    else:
        host.set_ylim((min(listv) - 0.1) * 0.9, (max(listv) + 0.1) * 1.1)

    plt.yticks(y_pos, mode, rotation=0, fontsize='small')

    nn = x_pos[::int(len(x_list) / 10)]
    xx = []
    for ii in nn:
        xx.append(x_list[ii][2:16])
    plt.xticks(nn, xx, rotation=15)

    host.set_xlabel(u'采样点')
    host.set_ylabel(u'单位：' + unit)
    par1.set_ylabel(u'模式')

    host.yaxis.label.set_color(p1.get_color())
    # host.yaxis.label.set_color(p3.get_color())
    par1.yaxis.label.set_color(p2.get_color())

    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    # host.tick_params(axis='y', colors=p3.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    lines = [p1, p2]
    #host.legend(lines, [l.get_label() for l in lines])
    #ax1.legend(loc=1, ncol=3, shadow=True)
    ss = filename##.decode('cp936')

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

def print_multi(x_list, unit, listv, listv1, dirname, filename, outdir, labels):
    mode = (u'待机', u'分发', u'', u'接收', u'提取', u'激光', u'')
    y_pos = np.arange(len(mode))
    x_pos = np.arange(len(x_list))
    plt.rc('figure', figsize=(18, 9))

    fig, host = plt.subplots()

    par1 = host.twinx()
    ps = []
    colors = ['b','k','y','c','g', 'm','lightpink','brown','orange','lightgreen','skyblue','purple','navy','darkgray','firebrick','plum','gold']
    styles = ['-',':','-.','--','-',':','-.','--','-',':','-.','--','-',':','-.','--']
    for i in range(len(labels)):
        print(i)
        print(len(listv),len(labels), len(listv[i::len(labels)]), labels[i])
        p1, = host.plot(range(0, len(listv)//len(labels)), listv[i::len(labels)], colors[i], label=labels[i], linestyle='-')
        ps.append(p1)
    p2, = par1.plot(range(0, len(listv1)), listv1, 'r-', label=u'工作模式')

    host.set_xlim(0, len(listv)//len(labels))
    if (filename.find('温度') > -1):
        if (filename.find('APD') > -1):
            host.set_ylim(-17, (max(listv) + 0.1) * 1.1)
        else:
            host.set_ylim(10, (max(listv) + 0.1) * 1.2)
    else:
        host.set_ylim((min(listv) - 0.1) * 0.9, (max(listv) + 0.1) * 1.1)

    plt.yticks(y_pos, mode, rotation=0, fontsize='small')

    nn = x_pos[::int(len(x_list) / 10)]
    xx = []
    for ii in nn:
        xx.append(x_list[ii][2:16])
    plt.xticks(nn, xx, rotation=15)

    host.set_xlabel(u'采样点')
    host.set_ylabel(u'单位：' + unit)
    par1.set_ylabel(u'模式')

    for i in range(1):#len(labels)):
        host.yaxis.label.set_color(ps[i].get_color())
    # host.yaxis.label.set_color(p3.get_color())
    par1.yaxis.label.set_color(p2.get_color())

    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=ps[0].get_color(), **tkw)
    #host.tick_params(axis='y', colors=p3.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    #lines = ps.append(p2)#[p1, p2, p3]
    host.legend(ps, [l.get_label() for l in ps], loc='upper left', ncol=len(ps)//4, shadow=True)
    #ax1.legend(loc=1, ncol=3, shadow=True)
    ss = filename##.decode('cp936')

    plt.title(ss[:ss.find('-')])
    if (filename.find('/') > 0):
        tt = filename.split('/')  # [filename.index('/')]='_'
        filename = tt[0] + tt[1]

    filename = filename.strip() + '.png'
    print(filename)
    pathname = os.path.join(outdir, filename)

    savefig(pathname)
    #plt.show()
    plt.clf()
    plt.close()

listmode = []
listmodetime = []
listmode_DTD = []
listmodetime_DTD = []
##对于CCU数据和PDHU数据全部绘图一遍
all_print_files = [merged_files[0], merged_files[-1]]
for ff in all_print_files:
    print("绘图文件:" + ff)
    reader = csv.reader(open(tmp_merge + ff, 'r'), delimiter=',', lineterminator='\n')
    header = reader.__next__()
    fig_dir = tmp_merge + 'all_data/' + ff[8:16] + '/'
    if (not os.path.exists(fig_dir)):
        os.makedirs(fig_dir)
    has_mode = 0
    if ff.find('CCU') > 0:
        header[12:28] = temper_name
        has_mode = 1
        print('ccu 文件', ff)
    has_mode_DTD = 0
    if ff.find('DTD') > 0:
        #header[12:28] = temper_name
        has_mode_DTD = 1
        print('DTD 文件', ff)
    data_array = []
    head_list = []
    list_tmp = []
    colums = len(header)
    j = 0
    aaa = ff.find('PDHU') or ff.find('DTD')
    print(aaa)

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
        if (has_mode == 1):
            ii = ((int(eval(row[1]))) & 0x1C) >> 2
            listmode.append(ii)
            listmodetime.append(row[0])
            for i in range(12, 28):
                list_tmp.append(float(row[i]))
        if (has_mode_DTD == 1):
            ii = ((int(eval(row[2]))) & 0x1C) >> 2
            listmode_DTD.append(ii)
            listmodetime_DTD.append(row[0])
    #new_list = []
    #aaa = ff.find('PDHU') | ff.find('DTD')

    for i in range(1, colums):
        listv = data_array[i - 1::colums - 1]
        # print listv
        if (has_mode_DTD > 0):
            #print('DTD 文件类型')
            print_csv(head_list, "", listv, listmode_DTD, fig_dir, header[i] + '-' + real_start + '-' + real_stop, fig_dir)
        else:
            #print('编号：', i)
            print_csv(head_list, "", listv, listmode, fig_dir, header[i] + '-' + real_start + '-' + real_stop, fig_dir)
    if (has_mode > 0):
        # listx = []
        # for ss in range(len(data_array)//(colums-1)):
        #     listx.append(data_array[ss*colums+11:ss*colums+27])
        #print(len(list_tmp), len(listmode), len(data_array))
        print_multi(head_list, "", list_tmp, listmode, fig_dir, '温度汇总' + '-' + real_start + '-' + real_stop, fig_dir, temper_name)

#####################################################
##对于所有数据仅在工作模式中绘图一遍
##根据listmode取得工作模式区间的索引
plt.plot(listmode)
plt.show()
mode_idx_list = []
new_mode = []
start_i = 0
len(listmode)
for ii in range(200, len(listmode)):
    if (listmode[ii - 5] == 0 and listmode[ii] > 0):
        start_i = ii - 20
    if (listmode[ii - 1] > 0 and listmode[ii] == 0):
        mode_idx_list.append([start_i, ii + 20])
        new_mode = new_mode + listmode[start_i:ii + 20]
        print(start_i, ii + 10)

mode_idx_list_DTD = []
new_mode_DTD = []
start_i = 0
for ii in range(200, len(listmode_DTD)):
    if (listmode_DTD[ii - 5] == 0 and listmode_DTD[ii] > 0):
        start_i = ii - 20
    if (listmode_DTD[ii - 1] > 0 and listmode_DTD[ii] == 0):
        mode_idx_list_DTD.append([start_i, ii + 20])
        new_mode_DTD = new_mode_DTD + listmode_DTD[start_i:ii + 20]
        print(start_i, ii + 10)
new_mode_tmp = new_mode
mode_idx_tmp = mode_idx_list
listmodetime_tmp = listmodetime
for ff in merged_files:
    if (len(mode_idx_list) == 0):
        print("当前时间段内没有工作模式" + ff)
        break
    print("绘图文件:" + ff)
    if(ff.find('DTD') > 0):
        print("DTD file")
        mode_idx_tmp = mode_idx_list_DTD
        listmodetime_tmp = listmodetime_DTD
        new_mode_tmp = new_mode_DTD
    else:
        mode_idx_tmp = mode_idx_list
        listmodetime_tmp = listmodetime
        new_mode_tmp = new_mode
    reader = csv.reader(open(tmp_merge + ff, 'r'), delimiter=',', lineterminator='\n')
    header = reader.__next__()
    fig_dir = tmp_merge + 'in_mode/' + ff[8:17] + '/'
    if (not os.path.exists(fig_dir)):
        os.makedirs(fig_dir)
    has_mode = 0
    if ff.find('CCU') > 0:
        header[12:28] = temper_name
    data_array = []
    head_list = []
    colums = len(header)
    j = 0

    for idx, row in enumerate(reader):
        if (len(row) < colums):
            continue
        head_list.append(row[0])
        for i in range(1, colums):
            if (row[i].find('0x') > -1):
                try:
                    data_array.append(float(eval(row[i])))
                except:
                    print(row[i], idx, ff)
            else:
                try:
                    aa = float(row[i])
                except:
                    aa = 0
                data_array.append(aa)

    new_list = []
    new_head = []
    ls_start = 0
    ls_end = len(head_list) - 1
    list_pos = []
    for ss, ee in mode_idx_tmp:
        ##二分法查找时间码对应的位置
        while (1):
            # 如果找到了中间值，即找到一个点
            tmp_pos = (ls_start + ls_end) // 2
            print(ls_start, ls_end, tmp_pos, head_list[tmp_pos], listmodetime_tmp[ss])
            if (head_list[tmp_pos].strip() > listmodetime_tmp[ss].strip()):
                ls_end = tmp_pos
            elif (head_list[tmp_pos].strip() < listmodetime_tmp[ss].strip()):
                ls_start = tmp_pos
            else:
                list_pos.append(tmp_pos)
                print(tmp_pos, head_list[tmp_pos])
                ls_end = tmp_pos
                break

            if (ls_start + 1 >= ls_end):
                list_pos.append(ls_end)
                print(ls_end, head_list[ls_end])
                break
        new_head.extend(head_list[ls_end:ls_end + ee - ss])
        ls_end = len(head_list) - 1
    new_head = []
    for ii, [ss, ee] in enumerate(mode_idx_tmp):
        new_head.extend(head_list[ss:ee])

    for i in range(1, colums):
        listv = data_array[i - 1::colums - 1]
        # print listv
        new_lst = []

        # new_mode = []
        for ii, [ss, ee] in enumerate(mode_idx_tmp):
            #new_lst.extend(listv[list_pos[ii]:list_pos[ii] + ee - ss])
            new_lst.extend(listv[ss:ee])

            # new_mode.extend(listmode[ss:ee])
            # print(len(new_mode), len(new_lst))
        #print("序列长度：",len(new_lst), len(new_head), len(new_mode_tmp))
        print_csv(new_head, "", new_lst, new_mode_tmp, fig_dir, header[i] + '-' + real_start + '-' + real_stop, fig_dir)
#####################################################


import zipfile


def zip_dir(dir_name, zipfile_name):
    file_list = []
    if (os.path.isfile(dir_name)):
        file_list.append(dir_name)
    else:
        for root, dirs, files in os.walk(dir_name):
            for name in files:
                file_list.append(os.path.join(root, name))
    zf = zipfile.ZipFile(zipfile_name, 'w', zipfile.zlib.DEFLATED)
    for tar in file_list:
        arcname = tar[len(dir_name):]
        zf.write(tar, arcname)
    zf.close()


print("zip directory:", tmp_merge)
zipfile_name = start_time + '-' + stop_time + '.zip'
zip_dir(tmp_merge, zipfile_name)
# print(ftp.pwd())
# aa = ftp.nlst(DRIN)
#    print(len(ftp.nlst()))

print("压缩完成")

# ##将压缩后的文件通过邮件发送出去
# import smtplib
# from email.mime.multipart import MIMEMultipart
# from email.mime.text import MIMEText
# from email.mime.image import MIMEImage
#
# sender = '327496031@163.com'
# receiver = ['ljt0132@ustc.edu.cn','qiangjia@mail.sitp.ac.cn']
# subject = '9XX CSV DATA'
# smtpserver = 'smtp.163.com'
# username = '327496031@163.com'
# password = 'xiangxin5linlin'
#
# msgRoot = MIMEMultipart('related')
# msgRoot['Subject'] = '9XX一周温度监测数据'
#
# #构造附件
# att = MIMEText(open(zipfile_name, 'rb').read(), 'base64', 'utf-8')
# att["Content-Type"] = 'application/octet-stream'
# att["Content-Disposition"] = 'attachment; filename="%s"'%zipfile_name
# msgRoot.attach(att)
#
# smtp = smtplib.SMTP()
# smtp.connect('smtp.163.com')
# smtp.login(username, password)
# smtp.sendmail(sender, receiver, msgRoot.as_string())
# smtp.quit()
#
# print("邮件发送完成")