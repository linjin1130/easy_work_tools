from DAboard import *
import filecmp

# import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.5.5'

##单板工作，测试检测
## 测试AD通过序列控制触发功能
## 测试序列控制循环模式
from DAboard import *
import data_waves
import math
import random
import matplotlib.pyplot as plt

#1一级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 4
loop_level = 0
seq_L1_low =  [loop_level,0,loop_cnt,ctrl]
loop_cnt = 10
seq_L1_nomal =  [loop_level,0,loop_cnt,ctrl]

#1一级触发输出停止单元
ctrl = 0x2 << 11
jump_addr = 1
loop_level = 0
seq_J1_low =  [loop_level,0,jump_addr,ctrl]

#1二级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 2
loop_level = 1
seq_L2_low =  [loop_level,0,loop_cnt,ctrl]
loop_cnt = 10
seq_L2_nomal =  [loop_level,0,loop_cnt,ctrl]

#1二级触发输出停止单元
ctrl = 0x2 << 11
jump_addr = 2
loop_level = 1
seq_J2_low =  [loop_level,0,jump_addr,ctrl]

#1三级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 2
loop_level = 2
seq_L3_low =  [loop_level,0,loop_cnt,ctrl]
loop_cnt = 10
seq_L3_nomal =  [loop_level,0,loop_cnt,ctrl]

#1三级触发输出停止单元
ctrl = 0x2 << 11
jump_addr = 3
loop_level = 2
seq_J3_low =  [loop_level,0,jump_addr,ctrl]

#1四级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 2
loop_level = 3
seq_L4_low =  [loop_level,0,loop_cnt,ctrl]
loop_cnt = 10
seq_L4_nomal =  [loop_level,0,loop_cnt,ctrl]

#1四级触发输出停止单元
ctrl = 0x2 << 11
jump_addr = 8
loop_level = 3
seq_J4_low =  [loop_level,0,jump_addr,ctrl]

#触发单元 正弦 周期为16个采样点
#触发类型，地址为0，长度为64ns ， 重复次数为0
ctrl = 0x8 << 11
start_addr = 0
length = 16
seq_T_low =  [start_addr,length,0,ctrl]

#计时输出单元  正弦波（周期为128个采样点）
#计时输出类型，地址为16，长度为128ns 计时2ns
ctrl = 0x4 << 11
start_addr = 16
length = 32
seq_D_low =  [start_addr,length,2,ctrl]

#态判断输出单元
ctrl = 0xC << 11
start_addr1 = 1#1态
start_addr2 = 1#2态
start_addr3 = 1#NULL态
start_addr4 = 1#0态
seq_C_low =  [start_addr1<<8 | start_addr2,64,start_addr3<<8 | start_addr4,ctrl]

da_ctrl = waveform()
# da_ctrl.generate_sin(cycle_count=1000)
# da_ctrl.generate_seq(length=len(da_ctrl.wave)>>4)
da_ctrl.gen_comp_wave()
# count_seq = [0, 64, 2, 4<<11]*2
tmp_wave = da_ctrl.wave[0:128]
da_ctrl.generate_sin(repeat=3,cycle_count=256)
tmp_wave += da_ctrl.wave[0:256]
# da_ctrl.generate_cos(repeat=3,cycle_count=256)
da_ctrl.generate_squr(repeat=4, hightime=320,lowtime1=160,lowtime2=160)
tmp_wave += da_ctrl.wave[0:640]
da_ctrl.wave = tmp_wave

# plt.figure()
# plt.plot(da_ctrl.wave)
# plt.show()

seq_T_stop=[0,16,0,seq_D_low[3]|(1<<15)]
temp_seq = seq_T_low+seq_L1_low+seq_L2_low+seq_L3_low+seq_D_low+seq_C_low+seq_J3_low+seq_J2_low+seq_L4_low+seq_D_low*2+seq_J4_low+seq_J1_low+seq_T_stop+[0,0,0,0]*4
temp_seq = seq_T_low+seq_L1_low+seq_L2_low+seq_D_low+seq_C_low+seq_J2_low+seq_J1_low+seq_T_stop+[0,0,0,0]*4
da_ctrl.seq = temp_seq
print(seq_T_low)
print(seq_C_low)
print(seq_D_low)
print(da_ctrl.seq)

sample_count = da_ctrl.wave_preview()
# print(da_ctrl.seq)
# print(da_ctrl.wave)
# plt.figure()
# plt.plot(wave)
# # plt.show()
# plt.figure()
# plt.plot(seq_mode)
# plt.show()

board_status = da.connect(new_ip)

da.MultiBoardMode(1) #1是单板工作
da.SetLoop(1,1,1,1)
da.SetDefaultVolt(1,32768)
da.SetDefaultVolt(2,32768)
da.SetDefaultVolt(3,32768)
da.SetDefaultVolt(4,32768)
da.SetTrigInterval(200*250)
da.SetTrigIntervalL2(200*250)
da.SetTrigCount(1)
da.SetTrigCountL2(1)
da.ClearTrigCount()
# # da_ctrl = waveform()
# da_ctrl.generate_sin(repeat=2,cycle_count=20000)
# da_ctrl.generate_seq(length=(len(da_ctrl.wave)>>3))
da.StartStop(240)
print(da_ctrl.seq)
da_ctrl.seq = [0, 16, 0, 16384, 0, 0, 2, 2048, 1, 0, 3, 2048, 2, 0, 2, 2048, 16, 32, 2, 8192, 257, 64, 257, 24576, 2, 0, 3, 4096, 1, 0, 2, 4096, 0, 0, 1, 4096, 0, 16, 2, 40960, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

for i in range(1):
    da.WriteSeq(1,da_ctrl.seq)
    da.WriteWave(1,da_ctrl.wave)
    da.WriteSeq(2,da_ctrl.seq)
    da.WriteWave(2,da_ctrl.wave)
    da.WriteSeq(3,da_ctrl.seq)
    da.WriteWave(3,da_ctrl.wave)
    da.WriteSeq(4,da_ctrl.seq)
    da.WriteWave(4,da_ctrl.wave)
    print(i)
    # da.SetTrigCount(10)
    da.SetDACStart(1)
    da.SetDACStop(5)
    da.SetTrigStart(2)
    da.SetTrigStop(6)
    da.StartStop(15)
    da.SendIntTrig()
    time.sleep(0.5)
    # da.StartStop(240)
    # time.sleep(1)

da.StartStop(240)
da.disconnect()
if board_status < 0:
    print('Failed to find board')