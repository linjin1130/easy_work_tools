from DAboard import *
import data_waves
import math
import random
# import matplotlib.pyplot as plt

#1一级触发输出开始单元
ctrl = 0x1 << 11
loop_cnt = 3
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
jump_addr = 3
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
jump_addr = 4
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
jump_addr = 5
loop_level = 3
seq_J4_low =  [loop_level,0,jump_addr,ctrl]


da_ctrl = waveform()
# da_ctrl.generate_sin(cycle_count=1000)
# da_ctrl.generate_seq(length=len(da_ctrl.wave)>>4)
da_ctrl.gen_comp_wave()
temp_seq = da_ctrl.seq[0:4]+seq_L1_low+seq_L2_low+seq_L3_low+da_ctrl.seq[4:12]+seq_J3_low+seq_J2_low+seq_L2_low+da_ctrl.seq[4:12]+seq_J2_low+seq_J1_low+da_ctrl.seq[12:]
da_ctrl.seq = temp_seq

print(da_ctrl.seq)
print(da_ctrl.wave)
wave, mode = da_ctrl.wave_preview()

# plt.figure()
# plt.plot(wave)
# plt.show()