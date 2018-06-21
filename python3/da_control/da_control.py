from DAboard import *
import filecmp

import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.2.5'

board_status = da.connect(new_ip)
# da.Run_Command(26,0,0)
# da.Init()
# da.InitBoard()
da.SetIsMaster(1)
# da.ClearTrigCount()
# time.sleep(1)
# da.SetLoop(1,2,3,4)
# da.SetGain(3, 123)
# rd_data = da.Read_RAM(0,1024)
# print(rd_data)
# wave = range(0,65536)#[1,2,3,1111,2222,2222]
# print(len(wave))

# da.Write_RAM(0,wave)
# da.StartStop(240)
# da.SetDefaultVolt(1,0)
# da.SetDefaultVolt(2,15000)
# da.SetDefaultVolt(3,30000)
# da.SetDefaultVolt(4,60000)
da_ctrl = waveform()
# da_ctrl.generate_seq()
da_ctrl.generate_sin(repeat=2048)
da_ctrl.generate_trig_seq(loopcnt=1024)
# print(len(da_ctrl.seq))
# print(len(da_ctrl.wave))
# print("wave")


# plt.figure()
# plt.plot(da_ctrl.wave)
# plt.show()
print(len(da_ctrl.wave))
cnt=0
for i in range(1000000):
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

    da.SetTrigCount(10)
    da.SendIntTrig()
    da.StartStop(15)
    time.sleep(2)

da.StartStop(240)
da.disconnect()
if board_status < 0:
    print('Failed to find board')