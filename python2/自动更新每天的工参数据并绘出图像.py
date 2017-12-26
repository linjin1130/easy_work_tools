# -*- coding: cp936 -*-
#1. FTP login
#2. get file directory
#3. get date
#4. copy data that gnerated from current date
#5. merge file
#6. plot every colonm data

#0. 设定定时任务自动执行上述过程

import ftplib
import os
import socket

HOST = 'localhost'
USER = 'user'
PASSWD = '12345'

DIRN = '\\tt\\test'

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

    try:
        ftp.cwd(DIRN)
    except ftplib.error_perm:
        print ('Error: cannot cd to "%s"' % DIRN)
        ftp.quit()
        return
    print ('*** Changed to "%s" folder' % DIRN)

    print(os.getcwd(), ftp.pwd())
    files = ftp.dir()
    files.sort()
    print(files)
    filename='DllTuixin1.h'
    try:
        ftp.retrbinary('RETR %s' % filename, open(filename, 'wb').write)
    except ftplib.error_perm:
        print ('ERROR: cannot read file "%s"' % filename)
        os.unlink(filename)
    else:
        print ('*** Downloaded "%s" to CWD' % filename)

    ftp.quit()
    return

if __name__ == '__main__':
    login_ftp()
