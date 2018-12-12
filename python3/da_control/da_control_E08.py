# from DAboard import *
# import filecmp
# import time
#
# import matplotlib.pyplot as plt
# da = DABoard()
# new_ip = '10.0.4.8'
#
# da2 = DABoard()
# new_ip2 = '10.0.5.2'
#
# board_status = da.connect(new_ip)
# board_status = da2.connect(new_ip2)
# # da.Run_Command(26,0,0)
# # da2 = da
# da.Init()
# da.InitBoard()
# da.SetIsMaster(1)
# # da.ClearTrigCount()
# # time.sleep(1)
# # da.SetLoop(1,2,3,4)
# # da.SetGain(3, 123)
# # rd_data = da.Read_RAM(0,1024)
# # print(rd_data)
# # wave = range(0,65536)#[1,2,3,1111,2222,2222]
# # print(len(wave))
#
# # da.Write_RAM(0,wave)
# # da.StartStop(240)
# # da.SetDefaultVolt(1,0)
# # da.SetDefaultVolt(2,15000)
# # da.SetDefaultVolt(3,30000)
# # da.SetDefaultVolt(4,60000)
# da_ctrl = waveform()
#
# da_ctrl.generate_pulse(dc_code=65535)
# # da_ctrl.generate_seq(length=len(da_ctrl.wave)>>3)
#
# da_ctrl.generate_trig_seq(loopcnt=10, repeat=200, length=(len(da_ctrl.wave)>>3)-8)
# print(da_ctrl.seq)
# print(da_ctrl.wave)
# # print("wave")
#
#
# # plt.figure()
# # plt.plot(da_ctrl.wave)
# # plt.show()
# da.GetEraseStatus()
# print(len(da_ctrl.wave))
# cnt=0
# for i in range(1000000):
#     da.WriteSeq(1,da_ctrl.seq)
#     da.WriteWave(1,da_ctrl.wave)
#     da.WriteSeq(2,da_ctrl.seq)
#     da.WriteWave(2,da_ctrl.wave)
#     da.WriteSeq(3,da_ctrl.seq)
#     da.WriteWave(3,da_ctrl.wave)
#     da.WriteSeq(4,da_ctrl.seq)
#     da.WriteWave(4,da_ctrl.wave)
#     cnt+=1
#     print(cnt)
#     da.StartStop(15)
#
#     da2.SetTrigCount(2000)
#     da2.SetTrigInterval(500000)
#     da2.SendIntTrig()
#
#     time.sleep(1)
#     da.StartStop(240)
#
#     time.sleep(1)
#     da.StartStop(240)
#
# da.StartStop(240)
# da.disconnect()
# if board_status < 0:
#     print('Failed to find board')

from .DAboard import *
from .data_waves import *
import filecmp

import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.4.8'

board_status = da.connect(new_ip)
# da.Run_Command(26,0,0)
# da.Init()
da.InitBoard()
da.SetLoop(1,1,1,1)
da.SetIsMaster(1)
da_ctrl = waveform()
# da_ctrl.generate_seq()
da_ctrl.generate_sin(repeat=32, cycle_count=8)
da_ctrl.generate_seq(length=len(da_ctrl.wave) >> 3)
da_ctrl.seq = [0, len(da_ctrl.wave)>>3, 0, 0x0000]*4096
# da_ctrl.generate_trig_seq(loopcnt=1024)
# print(len(da_ctrl.seq))
# print(len(da_ctrl.wave))
# print("wave")
da.SetGain(1,511)
da.SetGain(2,511)
da.SetGain(3,511)
da.SetGain(0,511)

# plt.figure()
# plt.plot(da_ctrl.wave)
# plt.show()
print(len(da_ctrl.wave))
cnt=0
for i in range(1):
    da.WriteSeq(1,da_ctrl.seq)
    da.WriteWave(1,da_ctrl.wave)
    da.WriteSeq(2,da_ctrl.seq)
    da.WriteWave(2,da_ctrl.wave)
    da.WriteSeq(3,da_ctrl.seq)
    da.WriteWave(3,da_ctrl.wave)
    da.WriteSeq(4,da_ctrl.seq)
    da.WriteWave(4,da_ctrl.wave)
    cnt+=1
    print(cnt)

    da.StartStop(240)

    da.SetTrigCount(1000)
    da.SendIntTrig()
    da.StartStop(15)
print(da_ctrl.seq)
# da.StartStop(240)
da.disconnect()
if board_status < 0:
    print('Failed to find board')