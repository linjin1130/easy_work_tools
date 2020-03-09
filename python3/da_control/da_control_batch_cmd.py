from da_board import *
from data_waves import *
import numpy as np
from seq_defines import *
import filecmp

import matplotlib.pyplot as plt

new_ip = '10.0.5.137'
da = DABoard(id='F157', ip=new_ip, data_offset=[0,0,0,0])
board_status = da.connect()
print(board_status)
# da.write_command(0xdeadbeef, 0, 0, donot_ret=True)
da.init_device()
# da.Run_Command(26,0,0)
# da.Init()
# da.InitBoard()
# da.SetIsMaster(1)
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
da_ctrl.generate_sin(repeat=8)

# da_ctrl.generate_seq()
da_ctrl.seq = generate_trig_seq(10, 2e-7, len(da_ctrl.wave), 0)
da_ctrl.wave = [32768]*32+da_ctrl.wave
da_ctrl.wave_preview()
# da_ctrl.generate_trig_seq(loopcnt=1024)
# print(len(da_ctrl.seq))
# print(len(da_ctrl.wave))
# print("wave")


# plt.figure()
# plt.plot(da_ctrl.wave)
# plt.show()
print(len(da_ctrl.wave))
cnt=0
# for i in range(1000000):
#     da.set_para(0x01, 0x234567, 0x89abcdef)
#     da.commit_para()
#     time.sleep(2)

print(len(da_ctrl.seq))
# _start = time.time()
# cycle_cnt = 1000
# for i in range(cycle_cnt):
#     da.write_seq(1,seq=da_ctrl.seq)
#     da.write_wave(1,wave=da_ctrl.wave)
#     da.write_seq(2,seq=da_ctrl.seq)
#     da.write_wave(2,wave=da_ctrl.wave)
#     da.write_seq(3,seq=da_ctrl.seq)
#     da.write_wave(3,wave=da_ctrl.wave)
#     da.write_seq(4,seq=da_ctrl.seq)
#     da.write_wave(4,wave=da_ctrl.wave)
#     cnt+=1
#     print(cnt)
#     #
#     # # da.stop_output_wave(0)
#     # da.set_trig_count_l1(10)
#     # da.start_output_wave(0)
#     # da.commit_para()
#     # da.wait_response()
#     # da.send_int_trig()
#     # da.wait_response()
#     # time.sleep(2)
# _stop = time.time()
#
# print(f'cycle count: {cycle_cnt}, 4 channel wave data and seq write is: {_stop-_start}')

da.set_monitor(1)

# da_ctrl.wave *= 2
# da_ctrl.wave = da_ctrl.wave[0:20000]
# da_ctrl.wave = [i for i in range(1024)]
# da_ctrl.seq = da_ctrl.seq[:32]
print(len(da_ctrl.wave))
# print(da_ctrl.wave)
# print(da_ctrl.seq)
da_ctrl.wave = np.asarray(da_ctrl.wave, dtype='<u2')
da_ctrl.seq = np.asarray(da_ctrl.seq, dtype='<u2')
_start = time.time()
cycle_cnt = 1000
for i in range(cycle_cnt):
    _s = time.time()
    for ch in range(4):
        da.write_seq_fast(ch+1,seq=da_ctrl.seq)
        da.write_wave_fast(ch+1,wave=da_ctrl.wave)

    _e = time.time()
    print(f'cnt:{cnt}, packet time 1 is:{_e-_s}')
    da.commit_mem_fast()
    _e = time.time()
    print(f'cnt:{cnt}, packet time 2 is:{_e-_s}')
    da.wait_response()
    cnt+=1
    _e = time.time()
    print(f'cnt:{cnt}, packet time 3 is:{_e-_s}')
    # print(cnt)
    #
    # da.stop_output_wave(0)
    da.set_trig_count_l1(60000)
    da.start_output_wave(1)
    da.start_output_wave(2)
    da.start_output_wave(3)
    da.start_output_wave(4)
    da.commit_para()
    da.wait_response()
    da.send_int_trig()
    # da.wait_response()
    _e = time.time()
    print(f'cnt:{cnt}, packet time is:{_e-_s}')
    # time.sleep(0.5)
_stop = time.time()

print(f'cycle count: {cycle_cnt}, fast 4 channel wave data and seq write is: {_stop-_start}')

# print(da.para_addr_list, da.para_data_list)
# da.stop_output_wave(0)
# print(da.para_addr_list, da.para_data_list)
# da.commit_para()
# da.wait_response()
da.disconnect()
if board_status < 0:
    print('Failed to find board')