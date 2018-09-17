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
    da_in.SpiReadWrite(0, reg_addr=9, reg_data=0)
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
codes = [0, 6392, 12539, 18204, 23169, 27244, 30272, 32137, 32767, 32137, 30272, 27244, 23169, 18204, 12539, 6392, 0, -6392, -12539, -18204, -23169, -27244, -30272, -32137, -32767, -32137, -30272, -27244, -23169, -18204, -12539, -6392]
def gen_and_send_wave(da):

    cnt = 0
    da_ctrl = waveform()
    # da_ctrl.generate_dc(dc_code=-1*0x2000,length=64,)
    da_ctrl.generate_sin(high=0x7FFF,offset=0,cycle_count=32)
    # da_ctrl.generate_pulse(dc_code=0)
    da_ctrl.generate_seq(length=len(da_ctrl.wave)>>3)
    # da_ctrl.generate_count_seq()
    da.StartStop(15)
    for code in codes:#range(-32767,32767,100):
        da_ctrl.generate_dc(dc_code=code,length=64,)
        da_ctrl.generate_seq(length=len(da_ctrl.wave)>>3)
        # print(da_ctrl.seq)
        # print(da_ctrl.wave[:32])
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
        print(code)
        # da.StartStop(15)
        time.sleep(0.05)
    # da_ctrl.generate_trig_seq(loopcnt=1024)
    print(len(da_ctrl.seq))
    # print(len(da_ctrl.wave))
    # print("wave")
    # da_ctrl.generate_pulse(dc_code=20000)
    # da_ctrl.generate_seq(length=len(da_ctrl.wave)>>3)
    # da_ctrl.generate_count_seq()
    print(da_ctrl.seq)
    print(da_ctrl.wave[:32])
    plt.figure()
    plt.plot(da_ctrl.wave)
    plt.show()
    print(len(da_ctrl.wave))
    cnt=0
    for i in range(100000):
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
        time.sleep(5)


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

volt = 0
da.SetDefaultVolt(4,volt)
da.SetDefaultVolt(1,volt)
da.SetDefaultVolt(2,volt)
da.SetDefaultVolt(3,volt)
da.StartStop(240)
gen_and_send_wave(da)
ltc200a_read_config(da)
da.disconnect()
if board_status < 0:
    print('Failed to find board')