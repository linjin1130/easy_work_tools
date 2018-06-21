import math
from itertools import repeat, chain
import numpy as np

class waveform:
    def __init__(self):
        self.amplitude = 65535
        self.defaultvolt = 20000
        self.frequency = 2e10
        self.seq = None
        self.wave = None
        self.generate_sin()

    def generate_seq(self, start_addr=0, length=40):
        unit = [start_addr,length,0,0]
        self.seq = unit*4096

    def generate_trig_seq(self, loopcnt=16, repeat=2000, start_addr=0, length=25):
        unit = [start_addr,length,repeat,1<<14]
        last = [start_addr,length,repeat,1<<15|1<<14]
        if repeat < 2:
            self.seq = last*loopcnt
        else:
            self.seq = unit*(loopcnt-1)+last
        print('序列长度：',len(self.seq))

    def generate_squr(self, repeat=0, lowtime1=0, hightime=100, lowtime2=100, low=0, high=65535):
        unit=[low]*lowtime1+[high]*hightime+[low]*lowtime2
        self.pad_unit(repeat, unit)

    def generate_sin(self, repeat=8, cycle_count=16, low=0, high=32767, offset=32768):
        unit = np.sin(np.arange(0, 2*np.pi, (2*np.pi)/cycle_count))*high+offset
        unit = unit.astype(np.int32)
        unit = list(unit)
        self.pad_unit(repeat, unit)

    def generate_dc(self, dc_code=32767):
        unit = [dc_code]*2048
        self.pad_unit(1, unit)

    def generate_saw(self, repeat=0, cycle_count=20, low=0, high=65535):
        unit = np.arange(low, high, (high-low)/cycle_count)
        self.pad_unit(repeat, unit)

    def pad_unit(self,repeat, unit):
        if repeat > 0:
            unit *= repeat
            seq_len = (len(unit)+7) >> 3
            pad_len = (32-(len(unit)&0x1F))&0x1F
            unit += [self.defaultvolt]*pad_len#32个采样点对齐
            self.generate_trig_seq(length=seq_len)
            self.wave = unit
        else:
            rep_map = [1,8,4,8,2,8,4,7]
            rep_len = rep_map[len(unit) & 0x7]
            unit = unit*(rep_len)
            seq_len = len(unit) >> 3
            print(seq_len)
            print("seq_len")
            pad_len = (32-(len(unit)&0x1F))&0x1F
            unit += [self.defaultvolt]*pad_len#32个采样点对齐
            self.generate_seq(length=seq_len)
            self.wave = unit
        # print(self.wave)
        print('波形长度：',len(self.wave))

# aa = waveform()
#
# import matplotlib.pyplot as plt
# plt.plot(aa.wave)
# plt.show()