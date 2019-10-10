import time
import datetime
from DAboard import *
from data_waves import *

new_ip = '192.168.2.12'
new_ip = '10.0.5.217'
# note = '失败'
# with open('配置记录.txt', 'a') as f:
#     f.write(','.join([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),new_ip, note, '呵呵']))

da = DABoard()

board_status = da.connect(new_ip)
# da.GetFlashType()
# da.DA_reset()
da.DA_reprog()
# da.InitBoard()
da.disconnect()