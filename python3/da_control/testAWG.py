from DAboard import *
import data_waves
import math
import random
import matplotlib.pyplot as plt

class WaveFormGenerator:
    def __init__(self):
        self.amplitude = 65535
        self.maxVoltage=500 #mV
        self.defaultvolt = 20000
        self.frequency = 2e10

    #amplitude mV
    #pattern 0-1
    def generateRawWave(self,pattern,repeat,amplitude):
        #patter=pattern*(amplitude*self.amplitude/self.maxVoltage)
        pattern=[int(pattern[x]*(amplitude*self.amplitude/self.maxVoltage)) for x in range(len(pattern))]
        pattern=pattern * repeat
        return pattern

    def packTo32(self, wave, vol):
        vol = int(vol * self.amplitude/self.maxVoltage)
        l=len(wave)
        pad=l % 32
        if pad>0:
            wave.append([vol]*(32-pad))

da=DABoard()
ip='10.0.3.25'
board_status = da.connect(ip)
da.SetIsMaster(1)
da.StartStop(0xF0)

da2=DABoard()
ip='10.0.5.5'
board_status = da2.connect(ip)
da2.SetIsMaster(1)
da2.StartStop(0xF0)

wg=WaveFormGenerator()
#wave1=wg.generateRawWave([1]*10+[0]*10, 10, 400)
wave1=wg.generateRawWave([1]*20, 10, 400)
wave1.extend(wg.generateRawWave([0],300,400))

wave1=wave1*8
wg.packTo32(wave1, 0)
# immediately run, repeat self
# seq1=[0,500,1,1<<15]
#1 length = 8 bit = 4ns
unit = [0,500,0,1<<14]
seq1 = unit*4096

print(wave1)

da.WriteSeq(1,seq1)
da.WriteWave(1,wave1)

wave2=wg.generateRawWave([1]*10+[0]*10, 25, 400)
wave2=wave2*8
wg.packTo32(wave2, 0)
# immediately run, repeat self
seq2=[0,500,0,1<<14]*4096
print(seq2)
da.WriteSeq(2,seq2)
da.WriteWave(2,wave2)

vol=[x/15 for x in range(15)]
wave3=[]
for i in range(5000):
    wave3.extend([random.choice(vol)]*20)

wave3=wg.generateRawWave(wave3,1,400)
wg.packTo32(wave3, 0)
seq3=[0,500,1,1<<14]*4096

da.WriteSeq(3,seq3)
da.WriteWave(3,wave3)

#the possibility we send 0 state
possi_0=0.9
wave4=[]
for i in range(5000):
    if random.random()<possi_0:
        wave4.extend([0]*20)
    else:
        wave4.extend([1]*10+[0]*10)

wave4=wg.generateRawWave(wave4,1,400)
wg.packTo32(wave4, 0)
seq4=[0,500,1,1<<14]*4096

da.WriteSeq(4,seq4)
da.WriteWave(4,wave4)

# plt.figure()
# plt.plot(wave1)
# # plt.show()
# plt.figure()
# plt.plot(wave2)
# # plt.show()
# plt.figure()
# plt.plot(wave3)
# # plt.show()
# plt.figure()
# plt.plot(wave4)
# plt.show()


da.SetTrigInterval(50000)
da.SetTrigCount(1000000)
da.StartStop(0x0F)

da.SendIntTrig()

da2.SetTrigInterval(50000)
da2.SetTrigCount(1000000)
da2.StartStop(0x0F)

da2.SendIntTrig()

