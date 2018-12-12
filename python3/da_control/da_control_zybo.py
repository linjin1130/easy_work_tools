import time
import matplotlib.pyplot as plt
from DAboard import *

# 连接设备
da = DABoard()
new_ip = '10.0.0.170'
board_status = da.connect(new_ip)

da_ctrl = waveform()

# 生成直流
da_ctrl.generate_sin()
da_ctrl.generate_trig_seq()

#自定义波形
# da_ctrl.wave = [60000]*1024 + [30000] * 10000
# da_ctrl.seq = [0,len(da_ctrl.wave) >> 3, 0, 0]*4096

#波形预览
# da_ctrl.wave_preview()

#写入波形到设备
# 先停止输出
da_ctrl.seq = da_ctrl.seq*1024*100
cycle_cnt = 10
bytes = len(da_ctrl.seq)
total = bytes*cycle_cnt

print(total)
print(time.time())



for i in range(cycle_cnt):
    da.WriteWave(4, da_ctrl.seq)
    # # 写入通道1 波形输出指令和波形
    # da.WriteSeq(1,da_ctrl.seq)
    # da.WriteWave(1,da_ctrl.wave)
    # # 写入通道2 波形输出指令和波形
    # da.WriteSeq(2,da_ctrl.seq)
    # da.WriteWave(2,da_ctrl.wave)
    # # 写入通道3 波形输出指令和波形
    # da.WriteSeq(3,da_ctrl.seq)
    # da.WriteWave(3,da_ctrl.wave)
    # # 写入通道4 波形输出指令和波形
    # da.WriteSeq(4,da_ctrl.seq)
    # da.WriteWave(4,da_ctrl.wave)
print(time.time())
#断开设备连接
da.disconnect()
if board_status < 0:
    print('Failed to find board')