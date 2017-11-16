# -*- coding:cp936 -*- 
import os
import csv
import ftplib
import socket
from datetime import date,timedelta,datetime
# import datetime
import time
DRLIST = ['CCU_','ATP_', 'PRD1','PRD2','DTD_']#'PPD_',
ST_name = ['分发模式','激光通信模式','接收模式','量子通信','QKD','ATP','EDFA','信标光','LD1','LD2','LD3','LD4']#统计参数名字
ST_COL  = [21,21,21,22,15,17,18,41,25,25,25,25]# 其所在列数
col_bit = [8,8,8,2,16,16,16,16,0,1,2,3]#所在列数的参数的bit位 =16表示浮点数， =8表示取模式位的低3位
comp_val = [1,2,2,1,10,10,3,1,1,1,1,1]
mask = [1,5,3,4,255,255,255,255,1,2,4,8]
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

delta_day = 1#获取多少天的数据
offset_day = 0
start_day = 0 ##与offset_day配合实现获取哪一天开始的数据
delta_stop = offset_day+start_day
delta_start = delta_stop+delta_day
start_time = "20"+(date.today()-timedelta(days=delta_start)).strftime("%y%m%d")+"120000"
stop_time  = "20"+(date.today()-timedelta(days=delta_stop)).strftime("%y%m%d")+"120000"

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
raw_dir = os.getcwd()+"/raw_data/"
merge_dir = os.getcwd()+"/merge_data/"
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
writer_sta_log = csv.writer(open(os.path.join(tmp_merge, '统计信息.log'), 'w'), delimiter=',', lineterminator='\n')
#writer_sta.writerow(('统计项目','开关次数','时间总和'))
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
            print('files to be merged:', s_file)
            reader = csv.reader(open(os.path.join(ss,s_file), 'r'), delimiter=',')
            if (start == 0):
                data = reader.__next__()
            else:
                start = 0
            for ii,row in enumerate(reader):
                if((ii%factor)==0):
                    writer.writerow(row)
                else:
                    if(is_DTD==1 and ii%4 == 1 and float(row[28])<1):#只对DTD文件处理,剔除异常数据
                        for i in range(0, len(pre_list)):
                            if(ST_COL[i] == 41):
                                cur_list[i] = int(float(row[ST_COL[i]]) * 2 + 0.1)
                            elif(col_bit[i] == 8):
                                cur_list[i] = 0
                                if((int(eval(row[ST_COL[i]])) & 7) == mask[i]):
                                    cur_list[i] = int(eval(row[ST_COL[i]])) & 7
                            # elif(mask[i] == 5):
                            #     if ((int(eval(row[ST_COL[i]])) ^ 7) == 5):
                            #         cur_list[i] = int(eval(row[ST_COL[i]])) ^ mask[i]
                            else:
                                cur_list[i] = int(eval(row[ST_COL[i]])) & mask[i]

                                #print(cur_list[i])
                            # if (col_bit[i] == 8):  # 模式
                            #     cur_list[i] = eval(row[ST_COL[i]]) % 7
                            #     if(cur_list[i] != 1):
                            #         cur_list[i] = 0
                            # elif (col_bit[i] == 9):  # 模式
                            #     cur_list[i] = eval(row[ST_COL[i]]) % 7
                            #     if(cur_list[i] != 5):
                            #         cur_list[i] = 0
                            # elif(ST_COL[i]==41):
                            #     cur_list[i] = int(float(row[ST_COL[i]]) * 2+0.1)
                            # elif (col_bit[i] == 16):  # 转为整数判断
                            #     cur_list[i] = int(float(row[ST_COL[i]]))
                            #     if(cur_list[i] < 4):
                            #         cur_list[i] = 0
                            # else:  # 比特位
                            #     cur_list[i] = int(eval(row[ST_COL[i]])) & (1 << col_bit[i])
                            delta = abs(cur_list[i] - pre_list[i])
                            if(delta >= comp_val[i]):
                                #if (delta >= 1):
                                evnt_list[i].append(row[0][:-6])#,cur_list[i]])
                                print(row[0],ST_name[i],cur_list[i], row[ST_COL[i]])
                                writer_sta_log.writerow((row[0],ST_name[i],cur_list[i], row[ST_COL[i]]))
                                # if(cur_list[i] < pre_list[i]):
                                #     cur_list[i] = 0
                                #     print('AIYA',row[07.187.5 ATP 27  27.176471],ST_name[i],cur_list[i], row[ST_COL[i]])
                        pre_list = cur_list.copy()


    merged_files.append(merged_filename)
    print(time.time())
    ##+'\\'+matched_files[-1][:matched_files[-1].index("_2")]
writer_sta = csv.writer(open(os.path.join(tmp_merge, '统计信息.csv'), 'w'), delimiter=',', lineterminator='\n')
writer_sta.writerow(('统计项目','开关次数','时间总和'))
for i,tt in enumerate(evnt_list):
    t_sta = tt[::2]
    t_end = tt[1::2]
    sum_t = datetime.strptime('2016-01-01 12:0:0', "%Y-%m-%d %H:%M:%S") - datetime.strptime('2016-01-01 12:0:0', "%Y-%m-%d %H:%M:%S")
    print(ST_name[i],tt)
    for j,te in enumerate(t_end):
        sum_t = sum_t+(datetime.strptime(te, "%Y-%m-%d %H:%M:%S") - datetime.strptime(t_sta[j], "%Y-%m-%d %H:%M:%S"))
        print(sum_t)
    writer_sta.writerow((ST_name[i], len(t_end), sum_t))
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
