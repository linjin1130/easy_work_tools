from DAboard import *
import filecmp
import time

import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.5.2'

board_status = da.connect(new_ip)
da.ClearTrigCount()

da.SetTrigInterval(250)#40ns,1us, 10us, 100us触发间隔
da.SetTrigCount(10)#10,100,1000触发次数
da.SetTrigIntervalL2(5*250)
da.SetTrigCountL2(10)

for i in range(1000000):#重复次数
    da.SendIntTrig()
    time.sleep(1)
    print(i)

da.disconnect()