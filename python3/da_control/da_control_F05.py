import time
import matplotlib.pyplot as plt
from DAboard import *
da = DABoard()
new_ip = '10.0.5.5'

board_status = da.connect(new_ip)
da.InitBoard()
da.SetGain(0, 511)
da.SetGain(1, 511)
da.SetGain(2, 511)
da.SetGain(3, 511)
da.SetLoop(1,1,1,1)

da_ctrl = waveform()
# da_ctrl.generate_pulse(dc_code=65535)
# da_ctrl.generate_count_seq()
da_ctrl.wave = [60000]*1024 + [30000] * 10000
da_ctrl.seq = [0,len(da_ctrl.wave) >> 3, 0, 0]*4096
plt.figure()
plt.plot(da_ctrl.wave)
plt.show()
# da_ctrl.wave_preview()
print(da_ctrl.seq)
cnt=0

for i in range(1):
    da.StartStop(240)
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
    # da.SetTrigInterval(200*250)
    # da.SetTrigIntervalL2(200*250)
    # da.SetTrigCount(1000)
    # da.SetTrigCountL2(1)
    da.StartStop(15)
    # da.SendIntTrig()
    time.sleep(1)

# da.StartStop(240)
da.disconnect()
if board_status < 0:
    print('Failed to find board')