from DAboard import *
import filecmp

import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.1.252'
da_ctrl = waveform()
def ltc2000a_spi_config(da_in):
    R_W = 1
    da_in.SpiReadWrite(0, reg_addr=1, reg_data=1)
    da_in.SpiReadWrite(0, reg_addr=3, reg_data=5)
    da_in.SpiReadWrite(0, reg_addr=4, reg_data=3)
    time.sleep(0.5)
    da_in.SpiReadWrite(0, reg_addr=4, reg_data=11)

def ltc200a_read_config(da_in):
    for i in range(0x20):
        data = da_in.SpiReadWrite(1, reg_addr=i)
        print(i, hex(data))
def ltc2000a_spi_config_pg(da_in):
    R_W = 1
    da_in.SpiReadWrite(0, reg_addr=2, reg_data=1)
    da_in.SpiReadWrite(0, reg_addr=4, reg_data=0)
    da_in.SpiReadWrite(0, reg_addr=30, reg_data=0)
    new_wave = da_ctrl.wave.copy()
    for i in range(64):

        new_wave[i] = 32767#da_ctrl.wave[i]>>1

        tt = struct.pack('h', new_wave[i])
        print(tt)
        da_in.SpiReadWrite(0, reg_addr=31, reg_data=new_wave[i]>>8)
        da_in.SpiReadWrite(0, reg_addr=31, reg_data=new_wave[i])
        print(i, new_wave[i])

    # plt.plot(new_wave)
    # plt.show()
    da_in.SpiReadWrite(0, reg_addr=30, reg_data=1)
    da_in.SpiReadWrite(0, reg_addr=4, reg_data=8)

def gen_and_send_wave(da):
    da_ctrl = waveform()
    # da_ctrl.generate_dc(dc_code=0x7F7F)
    da_ctrl.generate_sin(high=0x7FFF,offset=0)
    da_ctrl.generate_seq(length=len(da_ctrl.wave)>>3)
    print(da_ctrl.seq)
    # da_ctrl.generate_trig_seq(loopcnt=1024)
    print(len(da_ctrl.seq))
    # print(len(da_ctrl.wave))
    # print("wave")

    plt.figure()
    plt.plot(da_ctrl.wave)
    plt.show()
    print(len(da_ctrl.wave))
    cnt=0
    for i in range(1):
        da.WriteSeq(1,da_ctrl.seq)
        da.da_chip = 1
        da.WriteWave(1,da_ctrl.wave)
        da.da_chip = 0
        da.WriteSeq(2,da_ctrl.seq)
        da.da_chip = 1
        da.WriteWave(2,da_ctrl.wave)
        da.da_chip = 0
        da.WriteSeq(3,da_ctrl.seq)
        da.da_chip = 1
        da.WriteWave(3,da_ctrl.wave)
        da.da_chip = 0
        da.WriteSeq(4,da_ctrl.seq)
        da.da_chip = 1
        da.WriteWave(4,da_ctrl.wave)
        da.da_chip = 0
        cnt+=1
        print(cnt)
        da.StartStop(240)
        da.SetTrigCount(10)
        da.SendIntTrig()
        da.StartStop(15)

board_status = da.connect(new_ip)
da.StartStop(240)
da.SetDefaultVolt(4,0)
da.SetDefaultVolt(1,0)
da.SetDefaultVolt(2,0)
da.SetDefaultVolt(3,0)

ltc2000a_spi_config(da)
ltc200a_read_config(da)
# ltc2000a_spi_config_pg(da)
da.SpiReadWrite(0, reg_addr=2, reg_data=0)
# da.SpiReadWrite(0, reg_addr=4, reg_data=8)
ltc200a_read_config(da)
da.SetDefaultVolt(4,32768)
da.SetDefaultVolt(1,32768)
da.SetDefaultVolt(2,32768)
da.SetDefaultVolt(3,32768)
gen_and_send_wave(da)
ltc200a_read_config(da)
da.disconnect()
if board_status < 0:
    print('Failed to find board')