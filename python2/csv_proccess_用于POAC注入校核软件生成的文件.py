# -*- coding:cp936 -*- 
import os
import csv
from datetime import date,timedelta
import time
import datetime
merged_filename = "D:/Program Files/POAC/数据注入校核/ZRBM/20161013NS制作-晚上22点.csv"
print("merged file name:", merged_filename)
start = 1
writer = csv.writer(open(merged_filename[:len(merged_filename)-4]+'待比较.csv', 'w'), delimiter=',', lineterminator='\n')
log_filename = merged_filename[:len(merged_filename)-4]+'待比较.log'
log_wr = open(log_filename, 'w')
ground_station = {'FEA8557C0292007002737678':'兴隆','FF6865560359399C01B2C914':'丽江','FF97D70002FFAA44024BE4C8':'德令哈','0022DA5802C2BA44029A68C8':'南山','008EAD00032B6E900205C90C':'阿里'}

workmode = ["工作模式转换："]

temp_channel_close = ["关闭的温控通道："]
temp_channel_open = ["打开的温控通道："]
elc_open_time = ""
elc_close_time = ""

vlt_open_time = ""
vlt_close_time = ""

EDFA_open_time = ""
EDFA_close_time = ""

syn_channel = ""

xinbiao_open_time = ""
xinbiao_close_time = ""

QKD_open_time = ""
QKD_close_time = ""

ATP_open_time = ""
ATP_close_time = ""

comm_start_time = ""
comm_stop_time = ""

print ground_station['FEA8557C0292007002737678']

print('files to be merged:', merged_filename)
reader = ''
if(merged_filename.endswith('.csv')):
    reader = csv.reader(open(merged_filename, 'r'), delimiter=',', dialect=csv.excel)
else:
    reader = csv.reader(open(merged_filename, 'r'), delimiter='\t', dialect=csv.excel_tab)
line_num = 0
time_pre = date.today()
del_time = date.today()
print time.strftime("%Y/%m/%d %H:%M:%S", time.gmtime())
print(time_pre)

seconds = 0
curve_time = ""
instruction_count = 0
for row in reader:
    if(row[2] == ""):
        #print 'pass', row[1]
        continue
    instruction_count=instruction_count+1
    idx = row[2].find('地面站位置：')
    if(idx >= 0):
        station_str = row[2][idx:idx+36]
        print "iiiiiiiiiii:"+str(idx)
        log_wr.write(station_str+'\t')
        station_code = row[2][idx+12:idx+36]
        if ground_station.has_key(station_code):
            log_wr.write(ground_station[station_code]+'\n')
        else:
            log_wr.write('没有站点对应'+'\n')
    idx = row[2].find('注入序号N：01')
    if(idx > 0):
        tt = row[2].find('工作曲线数据：')
        curve_time = row[2][tt+14:tt+26]
        print curve_time[0:8]
        seconds=eval('0x'+curve_time[0:8])
        print seconds
        log_wr.write("曲线时间源码："+curve_time+"转换后的秒值："+str(seconds)+'\n')
    idx = row[2].find('开始量子通信')
    if(idx > 0):
        tt = row[2].find('执行时间：')
        tt2 = row[2].find('秒0000')
        com_time = row[2][tt+10:tt2]
        tt_time = com_time.split('天')
        tt3 = time.strptime(tt_time[1], "%H:%M:%S")
        print(tt_time[1])
        tt4 = tt3.tm_hour*3600+tt3.tm_min*60+tt3.tm_sec
        second_tt = int(tt_time[0])*24*3600+tt4
        print second_tt, tt4
        log_wr.write("通信时间源码："+com_time+"转换后的秒值："+str(second_tt)+"差值："+str(second_tt-seconds)+'\n')
		comm_start_time = row[1]
	
	if(row[2].find('停止量子通信')):
		comm_stop_time = row[1]
	
	if(row[2].find('控温通道关闭')):
		temp_channel_close.append('-'+row[1])
		
	if(row[2].find('控温通道打开')):
		temp_channel_open.append(row[1])
	idx = row[2].find('参数')
	if(row[2].find('工作模式转换')):
		workmode.append(row[1]+row[2][idx:])
	
	
    for ii in range(len(row)):
        if(len(row[ii])>0):
            index_start = row[ii].find('执行时间')
            index_stop = row[ii].find('0000（0.5毫秒）')
            if(index_start > 0 and index_stop > index_start):
                new_ss = row[ii][:index_start]+row[ii][index_stop+15:]
                row[ii] = new_ss
                
    if(line_num>1):
        #print time.strptime(row[1], "%Y/%m/%d %H:%M:%S"), time_pre
        #del_time = time.strptime(row[1], "%Y/%m/%d %H:%M:%S") - time_pre
        tt = time.strptime(row[1], "%Y/%m/%d %H:%M:%S")
        time_cur = time.mktime(tt)
        del_time = time_cur - time_pre
        #print del_time
    if(line_num>0):
        tt = time.strptime(row[1], "%Y/%m/%d %H:%M:%S")
        time_pre = time.mktime(tt)
        #print tt
        #print time_pre
    row[1] = del_time
    row[0] = ""
    line_num = line_num+1
    print line_num
    writer.writerow(row)


log_wr.write('事件个数：'+str((instruction_count-1))+'\n')
log_wr.close()
print 'end'
