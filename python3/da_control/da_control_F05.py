from DAboard import *
import filecmp

import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.5.5'

board_status = da.connect(new_ip)
# da.Run_Command(26,0,0)
# da.Init()
# da.InitBoard()
da.SetIsMaster(1)
da.SetLoop(1,1,1,1)
da.SetDefaultVolt(5,32768)
da.SetDefaultVolt(6,32768)
da.SetDefaultVolt(7,32768)
da.SetDefaultVolt(8,32768)
da_ctrl = waveform()
da_ctrl.generate_sin(repeat=1000)
# da_ctrl.gen_comp_wave()
# print(len(da_ctrl.seq))
# print(len(da_ctrl.wave))
print("wave")

# da_ctrl.gen_step_wave(steps=32)
# seq1 = da_ctrl.seq
# da_ctrl.gen_comp_wave(counter=20, length=256>>3)
# plt.figure()
# plt.plot(da_ctrl.wave)
# plt.show()
print(len(da_ctrl.wave))
print(len(da_ctrl.seq))

for i in range(1000):
    da.WriteSeq(1,da_ctrl.seq)
    da.WriteWave(1,da_ctrl.wave)
    da.WriteSeq(2,da_ctrl.seq)
    da.WriteWave(2,da_ctrl.wave)
    da.WriteSeq(3,da_ctrl.seq)
    da.WriteWave(3,da_ctrl.wave)
    da.WriteSeq(4,da_ctrl.seq)
    da.WriteWave(4,da_ctrl.wave)
    print(i)

    da.StartStop(240)

    # da.SetTrigCount(10)
    da.SetDACStart(1)
    da.SetDACStop(5)
    da.SetTrigStart(2)
    da.SetTrigStop(6)
    da.StartStop(10)
    da.SendIntTrig()
    time.sleep(1)

# da.StartStop(240)
da.disconnect()
if board_status < 0:
    print('Failed to find board')