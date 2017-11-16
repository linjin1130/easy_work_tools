# -*- coding:cp936 -*- 
import os
import csv
from datetime import date,timedelta
import time
import datetime
merged_filename = "D:/Program Files/POAC/����ע��У��/ZRBM/20161013NS����-����22��.csv"
print("merged file name:", merged_filename)
start = 1
writer = csv.writer(open(merged_filename[:len(merged_filename)-4]+'���Ƚ�.csv', 'w'), delimiter=',', lineterminator='\n')
log_filename = merged_filename[:len(merged_filename)-4]+'���Ƚ�.log'
log_wr = open(log_filename, 'w')
ground_station = {'FEA8557C0292007002737678':'��¡','FF6865560359399C01B2C914':'����','FF97D70002FFAA44024BE4C8':'�����','0022DA5802C2BA44029A68C8':'��ɽ','008EAD00032B6E900205C90C':'����'}

workmode = ["����ģʽת����"]

temp_channel_close = ["�رյ��¿�ͨ����"]
temp_channel_open = ["�򿪵��¿�ͨ����"]
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
    idx = row[2].find('����վλ�ã�')
    if(idx >= 0):
        station_str = row[2][idx:idx+36]
        print "iiiiiiiiiii:"+str(idx)
        log_wr.write(station_str+'\t')
        station_code = row[2][idx+12:idx+36]
        if ground_station.has_key(station_code):
            log_wr.write(ground_station[station_code]+'\n')
        else:
            log_wr.write('û��վ���Ӧ'+'\n')
    idx = row[2].find('ע�����N��01')
    if(idx > 0):
        tt = row[2].find('�����������ݣ�')
        curve_time = row[2][tt+14:tt+26]
        print curve_time[0:8]
        seconds=eval('0x'+curve_time[0:8])
        print seconds
        log_wr.write("����ʱ��Դ�룺"+curve_time+"ת�������ֵ��"+str(seconds)+'\n')
    idx = row[2].find('��ʼ����ͨ��')
    if(idx > 0):
        tt = row[2].find('ִ��ʱ�䣺')
        tt2 = row[2].find('��0000')
        com_time = row[2][tt+10:tt2]
        tt_time = com_time.split('��')
        tt3 = time.strptime(tt_time[1], "%H:%M:%S")
        print(tt_time[1])
        tt4 = tt3.tm_hour*3600+tt3.tm_min*60+tt3.tm_sec
        second_tt = int(tt_time[0])*24*3600+tt4
        print second_tt, tt4
        log_wr.write("ͨ��ʱ��Դ�룺"+com_time+"ת�������ֵ��"+str(second_tt)+"��ֵ��"+str(second_tt-seconds)+'\n')
		comm_start_time = row[1]
	
	if(row[2].find('ֹͣ����ͨ��')):
		comm_stop_time = row[1]
	
	if(row[2].find('����ͨ���ر�')):
		temp_channel_close.append('-'+row[1])
		
	if(row[2].find('����ͨ����')):
		temp_channel_open.append(row[1])
	idx = row[2].find('����')
	if(row[2].find('����ģʽת��')):
		workmode.append(row[1]+row[2][idx:])
	
	
    for ii in range(len(row)):
        if(len(row[ii])>0):
            index_start = row[ii].find('ִ��ʱ��')
            index_stop = row[ii].find('0000��0.5���룩')
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


log_wr.write('�¼�������'+str((instruction_count-1))+'\n')
log_wr.close()
print 'end'
