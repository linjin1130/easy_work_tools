# -*- coding: cp936 -*-
#2. get file directory
#2.1 ��ȡ��Ŀ¼
#2.2 ��ÿһ����Ŀ¼���д���
#2.2.1 ��ȡ�ļ�
#2.2.2 �ļ�����

import os
import csv
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
from datetime import datetime, date, timedelta

import ftplib
import os
import socket

HOST = 'localhost'
USER = 'user'
PASSWD = '12345'

DIRN = '/tt/test'

def login_ftp():
    try:
        ftp=ftplib.FTP(HOST)
    except (socket.error, socket.gaierror):
        print ('ERROR: cannot reach "%s"' % HOST)
        return
    print ('*** Connected to host "%s"' % HOST)

    try:
        ftp.login(USER, PASSWD)
    except ftplib.error_perm:
        print ('ERROR: login failed with "%s" and "%s"' % USER, PASSWD)
        ftp.quit()
        return
    print ('*** Logged in')
    return ftp, True

def logout_ftp(ftp):
    ftp.quit()
    return
from matplotlib.ticker import  MultipleLocator
from matplotlib.ticker import  FormatStrFormatter
def print_csv(x_list, unit, listv, listv1, dirname, filename, outdir):
    mode = (u'����', u'�ַ�', u'', u'����', u'��ȡ', u'����', u'',)
    y_pos = np.arange(len(mode))
    x_pos = np.arange(len(x_list))
    fig, host = plt.subplots()
    ##Create a figure with a set of subplots already made.
    ##This utility wrapper makes it convenient to create common layouts of
    ##subplots, including the enclosing figure object, in a single call.
    ##fig.subplots_adjust(right=0.75)##Tune the subplot layout.fig��subplots���ұ�λ�ã������ұ߶���0.75��λ�ó���

    par1 = host.twinx()
    p1, = host.plot(range(0,len(listv)), listv, "b-", label="����ֵ")
    p2, = par1.plot(range(0,len(listv1)), listv1, "r-", label="����ģʽ")
    #p3, = par2.plot([0, 1, 2], [50, 30, 15], "g-", label="Velocity")

    ##���ø���������귶Χ
    host.set_xlim(0, len(listv))
    if(filename.find('�¶�')>=0):
        if(filename.find('APD')<0):
            host.set_ylim(10, (max(listv)+0.1)*1.2)
        else:
            host.set_ylim(-17, (max(listv)+0.1)*1.2)
    else:
        host.set_ylim((min(listv)-0.1)*0.8, (max(listv)+0.1)*1.2)
    ##print (min(listv)-0.1), (max(listv)+0.1)
    plt.yticks(y_pos, mode, rotation=0 )
    xmajorLocator = MultipleLocator(int(len(x_list)/10))
    xminorLocator = MultipleLocator(5)
    #host.xaxis.set_major_locator(xmajorLocator)
    ##��ȡʱ��
    nn = x_pos[::int(len(x_list)/4)]
    xx = []
    for ii in nn:
        xx.append(x_list[ii][2:16])
    plt.xticks(nn, xx, rotation=10)
    #par1.set_ylim(0, 4)
    #par2.set_ylim(1, 20)

    ##���ø�������ǩ
    host.set_xlabel("������")
    host.set_ylabel("��λ��"+unit+"��")
    par1.set_ylabel("ģʽ")
    #par2.set_ylabel("Velocity")

    ##���ø�������ǩ����ɫ
    host.yaxis.label.set_color(p1.get_color())
    par1.yaxis.label.set_color(p2.get_color())
    #par2.yaxis.label.set_color(p3.get_color())

    ##���ø�����߿�����ɫ
    tkw = dict(size=4, width=1.5)
    host.tick_params(axis='y', colors=p1.get_color(), **tkw)
    par1.tick_params(axis='y', colors=p2.get_color(), **tkw)
    #par2.tick_params(axis='y', colors=p3.get_color(), **tkw)
    host.tick_params(axis='x', **tkw)

    #lines = [p1, p2, p3]
    lines = [p1,p2]
    ##����ͼ��
    host.legend(lines, [l.get_label() for l in lines])

    plt.title(filename[:filename.find('-')])
    filename = filename + '.png'
    pathname = os.path.join(outdir,filename)
    savefig(pathname)
    plt.clf()
    plt.close()

##��¼FTP
print("��¼FTP\n")
ftp, state = login_ftp()
if(state):
    try:
        ftp.cwd(DIRN)
    except ftplib.error_perm:
        print ('Error: cannot cd to "%s"' % DIRN)
    print ('*** Changed to "%s" folder' % DIRN)
    print(os.getcwd())
#dirs = "E:/Work/tt/test"
##files = os.listdir(dirs)
##��ȡ�ļ�Ŀ¼
print("��ȡ�ļ�Ŀ¼\n")
ftpfiles = ftp.mlsd()
files = []
for ff in ftpfiles:
    print(ff[0])
    files.append(ff[0])
files.sort()


print("ɸѡ�ļ�\n")
#2.2.3 ��������ɸѡ�ļ�
#��ȡ��ʼ��ֹͣ�����ַ���
print("��ȡ����\n")
delta_day = 3#Ҫ�ϲ����ļ���Խ������
offset_day = 22
start_day = 0
end_time   = "20" + (date.today()-timedelta(days=offset_day-start_day-delta_day)).strftime("%y%m%d")+"120000"##����12��Ϊ�յ�
start_time = "20" + (date.today()-timedelta(days=offset_day-start_day)).strftime("%y%m%d") + "120000"##ǰһ��12��Ϊ���
print (start_time, end_time)
#��ȡ�ļ����е���ʼʱ�䣬����ʱ��
##����ʹ���������������ļ�������������Ҫע���ļ�����������б����
matched_files = []
stop_idx = 0
start_idx = 0
find_start = 0
find_stop = 0
real_start = ""
real_stop = ""
print ("-------")
for s_file in files:
    strs = s_file.split('_')
    file_start = strs[-4]
    file_stop = strs[-3]
    print (s_file)
    print (file_start, file_stop)
    #����ļ���ʼʱ���Ѿ����������Ľ���ʱ�䣬�ҵ���ʼλ�ã���ֹ����
    if(file_start < start_time and file_stop > start_time and find_start == 0):
        start_idx = files.index(s_file)
        real_start = file_start
        find_start = 1
        print ("start", files.index(s_file))
    #����ļ�����ʱ���Ѿ����������Ŀ�ʼʱ�䣬�ҵ�����λ��
    if(file_start < end_time and file_stop > end_time):
        stop_idx = files.index(s_file)
        matched_files = files[start_idx:stop_idx+1]
        print ("stop", files.index(s_file))
        find_stop = 1
        break
    real_stop = file_stop

print ("-------")

print("����FTP��ɸѡ�õ��ļ�\n")##��ɸѡ�õ��ļ���FTP��������
raw_dir = os.getcwd()+"\\raw_data"
if(not os.path.exists(raw_dir)):
    os.makedirs(raw_dir)
if(find_stop == 0):
    matched_files = files[start_idx:]
for ff in matched_files:
    print(ff)
    target_file = raw_dir+'\\'+ff
    file_handle=open(target_file,"wb").write #��дģʽ�ڱ��ش��ļ�
    ftp.retrbinary('RETR ' + ff, file_handle, 1024)
    #ftp.retrbinary("RETR ff",file_handle) #���շ��������ļ���д�뱾���ļ�

##�˳�FTP��¼
print("�˳�FTP\n")
logout_ftp(ftp)
##


print("�ϲ��ļ�\n")
#2.2.4 �ϲ��ļ�
merged_dir = os.getcwd()+"\\"+matched_files[-1][:matched_files[-1].index("_2")]+"\\"+real_start+'_'+real_stop
if(not os.path.exists(merged_dir)):
    os.makedirs(merged_dir)
merged_filename = files[-1][:files[-1].index("_2")]+'_'+real_start+'_'+real_stop+".csv"

print("��ȡ�ļ����б�\n")
if(len(matched_files)>0):
    print (os.path.join(merged_dir,merged_filename))
    writer = csv.writer(open(os.path.join(merged_dir,merged_filename), "w"), delimiter=',', lineterminator='\n')
    start = 1
    for s_file in matched_files:
        reader = csv.reader(open(raw_dir+'\\'+s_file, "r"), delimiter=',')
        if(start == 0):
            data = reader.__next__()
        else:
            start = 0
        for row in reader:
            writer.writerow(row)
else:
    print(r"û���ļ�")
##���ϲ�����ļ����л�ͼ
reader = csv.reader(open(os.path.join(merged_dir,merged_filename), "r"), delimiter=',', skipinitialspace=True, lineterminator='\n')
##��һ�����������ݵ�����
header = reader.__next__()
dataarry = []
headarry = []
colums = len(header)
##��������һ������������ݵ��б���
# print("���ж�ȡ�ļ�\n")
for rows in reader:
    headarry.append(rows[0])
    for i in range(1, colums):
        if(rows[i].startswith('0x') < 1):
            dataarry.append(float(rows[i]))
        else:
            dataarry.append(float(eval(rows[i])))
            #print (rows[i], float(eval(rows[i])))
##��ÿһ�����ݻ�ͼ
print("��ÿһ�����ݻ�ͼ\n")
for i in range(1, colums):
    listv = dataarry[i-1::colums-1]
    ##print(listv)
    listmode = []

    print_csv(headarry, "", listv, listmode, merged_dir, header[i]+'-'+real_start+'_'+real_stop, merged_dir)

##����ȡ��ϲ��������Լ����ɵ�ͼƬѹ��
import zipfile

print("ѹ���ļ�\n")
def zip_dir(dirname,zipfilename):
    filelist = []
    if os.path.isfile(dirname):
        filelist.append(dirname)
    else :
        for root, dirs, files in os.walk(dirname):
            for name in files:
                filelist.append(os.path.join(root, name))

    zf = zipfile.ZipFile(zipfilename, "w", zipfile.zlib.DEFLATED)
    for tar in filelist:
        arcname = tar[len(dirname):]
        #print arcname
        zf.write(tar,arcname)
    zf.close()

zipfile_name = os.path.join(os.getcwd(),merged_filename[:merged_filename.index(".csv")]+".zip")
zip_dir(merged_dir, zipfile_name)
print("ѹ�����")

##��ѹ������ļ�ͨ���ʼ����ͳ�ȥ
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage

sender = '327496031@163.com'
receiver = 'jin.lin@quantum-info.com'
subject = '9XX CSV DATA'
smtpserver = 'smtp.163.com'
username = '327496031@163.com'
password = 'xiangxin5linlin'

msgRoot = MIMEMultipart('related')
msgRoot['Subject'] = 'test message'

#���츽��
att = MIMEText(open(zipfile_name, 'rb').read(), 'base64', 'utf-8')
att["Content-Type"] = 'application/octet-stream'
att["Content-Disposition"] = 'attachment; filename="%s"'%zipfile_name
msgRoot.attach(att)

smtp = smtplib.SMTP()
smtp.connect('smtp.163.com')
smtp.login(username, password)
smtp.sendmail(sender, receiver, msgRoot.as_string())
smtp.quit()
