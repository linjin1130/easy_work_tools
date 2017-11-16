# -*- coding: cp936 -*-
#2. get file directory
#2.1 获取子目录
#2.2 对每一个子目录进行处理
#2.2.1 获取文件
#2.2.2 文件排序

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