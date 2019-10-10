from DAboard import *
from data_waves import *

import matplotlib.pyplot as plt

new_ip = ['10.0.5.4','10.0.5.5','10.0.5.2']#,'10.0.5.2','10.0.5.6','10.0.5.7']
new_ip = ['10.0.5.188']#,'10.0.5.2','10.0.5.6','10.0.5.7']

das = [None]*len(new_ip)
for idx in range(len(new_ip)):
    das[idx] = DABoard()
    print(new_ip[idx])
    das[idx].connect(new_ip[idx])
    das[idx].InitBoard()

for da in das:
    da.SetIsMaster(0)
    da.SetTrigSel(3)
    da.SetLoop(1,1,1,1,)
    da.SetTrigInterval(200 * 250)
    da.SetTrigIntervalL2(200 * 250)
    da.SetTrigCount(10000)
    da.SetTrigCountL2(10000)
    da.SetTrigStart(1)
    da.SetTrigStop(10)
    da.SetGain(0,511)
    da.SetGain(1,511)
    da.SetGain(2,511)
    da.SetGain(3,511)

das[0].SetIsMaster(1)
da_ctrl = waveform()
# da_ctrl.generate_seq()
da_ctrl.generate_sin(repeat=2048, cycle_count = 8, low=0, high=32767)
da_ctrl.generate_seq(length=len(da_ctrl.wave) >> 3)
# da_ctrl.generate_squr()
# da_ctrl.seq = [0, len(da_ctrl.wave)>>3, 0, 0x4000]*4096
# da_ctrl.generate_trig_seq(loopcnt=4096)
cnt = 0
for i in range(1):
    for da in das:
        da.StartStop(240)
        for ch in range(1,5):
            da.WriteSeq(ch,da_ctrl.seq)
            da.WriteWave(ch,da_ctrl.wave)
        da.StartStop(15)
    cnt+=1
    print(cnt)

das[0].SendIntTrig()

for da in das:
    da.disconnect()
