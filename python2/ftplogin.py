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

HOST = '9.9.9.9'
USER = 'lzmy'
PASSWD = 'lzmylzmy'

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
        print ('ERROR: login failed with "%s" and "%s"' %USER %PASSWD)
        ftp.quit()
        return
    print ('*** Logged in')
    return ftp, True

def logout_ftp(ftp):
    ftp.quit()
    return

ftp, state = login_ftp()
ftp.dir()
logout_ftp(ftp)