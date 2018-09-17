from DAboard import *
import filecmp

import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.5.2'

board_status = da.connect(new_ip)
# da.Run_Command(26,0,0)
da.Init()
# da.InitBoard()
# da.SetIsMaster(1)
# da.ClearTrigCount()
# time.sleep(1)
# da.SetLoop(1,2,3,4)
da.SetGain(0, 580)
da.SetGain(1, 580)
da.SetGain(2, 580)
da.SetGain(3, 580)
da.SetLoop(5,5,5,5)
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
# da_ctrl.generate_sin(repeat=10,cycle_count=16, high=32767)
# da_ctrl.generate_seq(length=len(da_ctrl.wave)>>3)
# da_ctrl.gen_reset_control_wave_seq()

da_ctrl.generate_pulse(dc_code=0)
da_ctrl.generate_trig_seq(loopcnt=1000,repeat=12,length=len(da_ctrl.wave)>>3)
# print(len(da_ctrl.seq))
# print(len(da_ctrl.wave))
# print("wave")
da_ctrl.load_wave_file()
wave1 = da_ctrl.wave
da_ctrl.generate_pulse(dc_code=0)
# da_ctrl.generate_seq(length=len(da_ctrl.wave)>>3)
da_ctrl.generate_count_seq()

# da_ctrl.wave[10000:30000] = wave1[0:20000]


# plt.figure()
# plt.plot(da_ctrl.wave)
# plt.show()
# print(len(da_ctrl.wave))
# print(da_ctrl.seq)
cnt=0

for i in range(1000):
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
    da.SetTrigInterval(200*250)
    da.SetTrigIntervalL2(200*250)
    da.SetTrigCount(1000)
    da.SetTrigCountL2(1)
    da.StartStop(15)
    da.SendIntTrig()
    time.sleep(1)


# da.StartStop(240)
da.disconnect()
if board_status < 0:
    print('Failed to find board')