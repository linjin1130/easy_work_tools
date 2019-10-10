import time

from DAboard import *
from data_waves import *
import filecmp

import matplotlib.pyplot as plt

da = DABoard()
da_master = DABoard()
new_ip = '10.0.5.113'
master_ip = '10.0.5.217'

board_status = da.connect(new_ip)
board_status = da_master.connect(master_ip)
# da.Run_Command(26,0,0)
# da.Init()
# da.InitBoard()

da.MultiBoardMode(0)
da_ctrl = waveform()
da_ctrl.generate_trig_seq(loopcnt=1024)
# print(len(da_ctrl.seq))
# print(len(da_ctrl.wave))
# print("wave")

bad_seq = [0 ,          4 ,        10  ,     16384  ,       772 ,         25 ,       258   ,    24576  ,       320, 63 ,         99  ,      8192 ,          0  ,         25  ,         1  ,     49152]

d_seq = [512*5 >> 3, 63, 2, 4 << 11]
t_seq = [512*3 >> 3,4,10,0x8<<11]
stop_seq = [512*0 >> 3,25,1,0x8<<11 | 0x8000]
c_seq = [0x0101, 25, 0x0101, 0xC<<11]
da_ctrl.seq = t_seq + d_seq+ c_seq + d_seq+ stop_seq
# da_ctrl.seq = bad_seq
da_ctrl.seq *= 8
# da_ctrl.seq = [512*2 >> 3,25,20,0x8<<11, 512*3 >> 3, 25, 20, (0x8<<11) | 0x8000] * 32
# da_ctrl.seq = [512*4 >> 3,25,20,0x8<<11, 512*5 >> 3, 25, 20, (0x8<<11) | 0x8000] * 32
# plt.figure()
# plt.plot(da_ctrl.wave)
# plt.show()
print(da_ctrl.seq)
cnt=0
for i in range(100):
    da.WriteSeq(1,da_ctrl.seq)
    da.WriteSeq(2,da_ctrl.seq)
    da.WriteSeq(3,da_ctrl.seq)
    da.WriteSeq(4,da_ctrl.seq)
    cnt+=1
    print(cnt)
    da.StartStop(240)

    da.SetTrigCount(10)
    da.StartStop(15)
    da_master.SendIntTrig()
    time.sleep(0.3)

da.StartStop(240)
da.disconnect()
da_master.disconnect()
if board_status < 0:
    print('Failed to find board')