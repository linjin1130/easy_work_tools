import time
import matplotlib.pyplot as plt
from UDPDAboard import *
from data_waves import *
# 连接设备
da = UDPDABoard()
new_ip = '10.0.0.129'
board_status = da.connect(new_ip)

# 初始化
da.InitBoard()
#设置增益，默认电压，循环次数等运行参数，
da.SetGain(0, 511)
da.SetGain(1, 511)
da.SetGain(2, 511)
da.SetGain(3, 511)
da.SetLoop(1,1,1,1)
# da.SetDefaultVolt(0,32768)
# da.SetDefaultVolt(1,32768)
# da.SetDefaultVolt(2,32768)
# da.SetDefaultVolt(3,32768)

# 定义波形
da_ctrl = waveform()

# 生成直流
da_ctrl.generate_sin(repeat=64, cycle_count=8)
da_ctrl.generate_seq()
# da_ctrl.generate_seq()

#自定义波形
# da_ctrl.wave = [60000]*1024 + [30000] * 10000
# da_ctrl.seq = [0,len(da_ctrl.wave) >> 3, 0, 0]*4096

#波形预览
# da_ctrl.wave_preview()

#写入波形到设备
# 先停止输出

for i in range(1):
    _start = time.time()
    da.StartStop(240)
    # 写入通道1 波形输出指令和波形
    da.WriteSeq(1,da_ctrl.seq)
    da.WriteWave(1,da_ctrl.wave)
    # 写入通道2 波形输出指令和波形
    da.WriteSeq(2,da_ctrl.seq)
    da.WriteWave(2,da_ctrl.wave)
    # 写入通道3 波形输出指令和波形
    da.WriteSeq(3,da_ctrl.seq)
    da.WriteWave(3,da_ctrl.wave)
    # 写入通道4 波形输出指令和波形
    da.WriteSeq(4,da_ctrl.seq)
    da.WriteWave(4,da_ctrl.wave)

    # 设置触发间隔
    da.SetTrigInterval(200*250)
    # 设置触发次数
    da.SetTrigCount(1000)
    # 使能输出
    da.StartStop(15)
    # 使能触发
    # da.SendIntTrig()
    # time.sleep(1)
    _end = time.time()
    print(f'test count:{i}, time:{round(_end-_start, 5)}')

#断开设备连接
da.disconnect()
print('end')