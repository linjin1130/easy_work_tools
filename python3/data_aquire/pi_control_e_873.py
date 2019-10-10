#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This example helps you to define arbitrary waveforms read out from a file."""
import time
from time import sleep

from pipython import GCSDevice, pitools

CONTROLLERNAME = 'E-873'
STAGES = None  # connect stages to axes
REFMODE = None  # reference the connected stages

DATAFILE = r'wavegenerator_pnt.txt'
NUMCYLES = 1 # number of cycles for wave generator output
TABLERATE = 100  # duration of a wave table point in multiples of servo cycle times as integer
ip = '172.16.0.36'

e_873 = GCSDevice(CONTROLLERNAME)
e_873.ConnectTCPIP(ipaddress=ip, ipport=50000)
print('connected: {}'.format(e_873.qIDN().strip()))
print('initialize connected stages...')
print(e_873.axes)
# pitools.startup(e_873, stages=STAGES, refmode=REFMODE)

e_873.MOV(e_873.axes[1], 7.5)
for i in range(75):
    e_873.MOV(e_873.axes[1], i*0.1)
    time.sleep(0.2)
    print(i)
# To check the on target state of an axis there is the GCS command
# qONT(). But it is more convenient to just call "waitontarget".

# pitools.waitontarget(e_873)
e_873.CloseConnection()