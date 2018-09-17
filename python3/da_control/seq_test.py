from DAboard import *
import filecmp

import matplotlib.pyplot as plt

da_ctrl = waveform()
da_ctrl.generate_sin(repeat=128>>4, cycle_count=16, pad=1)
wave_sin = da_ctrl.wave
da_ctrl.generate_cos(repeat=128>>4, cycle_count=16, pad=1)
wave_cos = da_ctrl.wave
da_ctrl.generate_dc(dc_code=0, length=384, pad=1)
wave_dc_lowx384 = da_ctrl.wave
da_ctrl.generate_dc(dc_code=65535, length=512, pad=1)
wave_dc_highx512 = da_ctrl.wave
da_ctrl.generate_squr(repeat=128>>4, lowtime1=4, hightime=8, lowtime2=4, pad=1)
wave_squr = da_ctrl.wave
da_ctrl.generate_saw(repeat=128>>4, cycle_count=16, pad=1)
wave_saw = da_ctrl.wave
da_ctrl.generate_inv_saw(repeat=128>>4, cycle_count=16, pad=1)
wave_saw_inv = da_ctrl.wave

da_ctrl.generate_sin(repeat=0, cycle_count=100000, pad=1)
wave_sin_50u = da_ctrl.wave

waves = [wave_sin, wave_cos, wave_saw_inv, wave_saw,wave_squr]
da_ctrl.wave = []
for wave in waves:
    # print('ooooo')
    da_ctrl.wave.extend(wave)
    da_ctrl.wave = da_ctrl.wave+wave_dc_lowx384
    da_ctrl.wave = da_ctrl.wave+wave_dc_highx512
    # print(da_ctrl.wave)
wave_total = da_ctrl.wave
#触发单元 正弦
#触发类型，地址为0，长度为8ns,50us, 64ns ， 重复次数为0
ctrl = 0x8 << 11
start_addr = 0
seq_T_low =  [start_addr,2,0,ctrl]
seq_T_high =  [start_addr,100000>>3,0,ctrl]
seq_T_nomal =  [start_addr,128>>3,0,ctrl]

# 余弦
#触发类型，地址为1024，长度为8ns,50us, 64ns ， 重复次数为0
start_addr = 1024>>3
seq_T1_low =  [start_addr,2,0,ctrl]
seq_T1_high =  [start_addr,100000>>3,0,ctrl]
seq_T1_nomal =  [start_addr,128>>3,0,ctrl]

#触发类型，地址为0，长度为2， 重复次数分别为1 2 3
start_addr = 0
seq_T2_low =  [start_addr,2,1,ctrl]
seq_T2_high =  [start_addr,100000>>3,2,ctrl]
seq_T2_nomal =  [start_addr,128>>3,3,ctrl]

#直接输出单元 余弦波
#直接输出类型，地址为0，长度为8ns,50us, 64ns
ctrl = 0x0 << 11
start_addr = 2048>>3
seq_S_low =  [start_addr,2,0,ctrl]
seq_S_high =  [start_addr,100000>>3,0,ctrl]
seq_S_nomal =  [start_addr,128>>3,0,ctrl]

#计时输出单元  方波
#计时输出类型，地址为0，长度为8ns，计时8ns;,50us,计时40us; 64ns, 计时40ns
ctrl = 0x4 << 11
start_addr = 2048>>3
seq_D_low =  [start_addr,2,2,ctrl]
seq_D_high =  [start_addr,100000>>3,10000,ctrl]
seq_D_nomal =  [start_addr,128>>3,10,ctrl]

#态判断输出单元
ctrl = 0xC << 11
start_addr1 = 0#1态
start_addr2 = 2#2态
start_addr3 = 4#NULL态
start_addr4 = 6#0态
seq_C_low =  [start_addr1<<8 | start_addr2,2,start_addr3<<8 | start_addr4,ctrl]
seq_C_high =  [start_addr1<<8 | start_addr2,100000>>3,start_addr3<<8 | start_addr4,ctrl]
seq_C_nomal =  [start_addr1<<8 | start_addr2,128>>3,start_addr3<<8 | start_addr4,ctrl]
seq_C_low =  [start_addr2<<8 | start_addr3,2,start_addr4<<8 | start_addr1,ctrl]
seq_C_low =  [start_addr3<<8 | start_addr4,2,start_addr1<<8 | start_addr2,ctrl]
seq_C_low =  [start_addr4<<8 | start_addr1,2,start_addr2<<8 | start_addr3,ctrl]
# seq_C_low =  [2,4,65535,ctrl]

#1一级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 1
loop_level = 0
seq_L1_low =  [loop_level,0,loop_cnt,ctrl]
loop_level = 10
seq_L1_nomal =  [loop_level,0,loop_cnt,ctrl]

#1一级触发输出停止单元
ctrl = 0x2 << 11
jump_addr = 2
loop_level = 0
seq_J1_low =  [loop_level,0,jump_addr,ctrl]

#1二级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 1
loop_level = 1
seq_L2_low =  [loop_level,0,loop_cnt,ctrl]
loop_level = 10
seq_L2_nomal =  [loop_level,0,loop_cnt,ctrl]

#1二级触发输出停止单元
ctrl = 0x2 << 11
jump_addr = 3
loop_level = 1
seq_J2_low =  [loop_level,0,jump_addr,ctrl]

#1三级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 1
loop_level = 2
seq_L3_low =  [loop_level,0,loop_cnt,ctrl]
loop_level = 10
seq_L3_nomal =  [loop_level,0,loop_cnt,ctrl]

#1三级触发输出停止单元
ctrl = 0x2 << 11
jump_addr = 4
loop_level = 2
seq_J3_low =  [loop_level,0,jump_addr,ctrl]

#1四级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 1
loop_level = 3
seq_L4_low =  [loop_level,0,loop_cnt,ctrl]
loop_level = 10
seq_L4_nomal =  [loop_level,0,loop_cnt,ctrl]

#1四级触发输出停止单元
ctrl = 0x2 << 11
jump_addr = 5
loop_level = 3
seq_J4_low =  [loop_level,0,jump_addr,ctrl]

da = DABoard()
new_ip = '10.0.5.2'
board_status = da.connect(new_ip)
# da.Run_Command(26,0,0)
da.Init()
da.InitBoard()
da.SetGain(0, 511)
da.SetGain(1, 511)
da.SetGain(2, 511)
da.SetGain(3, 511)
da.SetTrigStart(2)
da.SetDefaultVolt(1, 32768)
da.SetDefaultVolt(2, 32768)
da.SetDefaultVolt(3, 32768)
da.SetDefaultVolt(4, 32768)

seq_count = 1
#########################################################
#测试49
#触发1次 循环3次 下限长度
da_ctrl.seq.clear()
da_ctrl.seq = seq_T_low +seq_D_low+seq_C_low
# da_ctrl.seq = da_ctrl.seq+seq_T1_low
da_ctrl.seq[-1] |= 32768
da_ctrl.seq += [0,0,0,0]*10
da_ctrl.wave = wave_total
loopcnt = 3
trig_seq_cnt = 1
seq_count = 3
trig_count = loopcnt * trig_seq_cnt
da.SetLoop(loopcnt,loopcnt,loopcnt,loopcnt)
#########################################################

print(da_ctrl.seq)
da.StartStop(240)
da.WriteSeq(1,da_ctrl.seq)
da.WriteWave(1,da_ctrl.wave)
da.WriteSeq(2,da_ctrl.seq)
da.WriteWave(2,da_ctrl.wave)
da.WriteSeq(3,da_ctrl.seq)
da.WriteWave(3,da_ctrl.wave)
da.WriteSeq(4,da_ctrl.seq)
da.WriteWave(4,da_ctrl.wave)
trig_interval = max(10,da_ctrl.seq[1])
if trig_interval < 58:
    da.SetTrigStart(trig_interval-1)
    print('触发间隔过小',trig_interval)
da.SetTrigInterval((trig_interval + 4)* seq_count)
da.SetTrigIntervalL2((trig_interval + 4)* seq_count)
da.SetTrigCount(trig_count)
da.SetTrigCountL2(1)
da.StartStop(15)
da.SendIntTrig()

da.disconnect()
if board_status < 0:
    print('Failed to find board')