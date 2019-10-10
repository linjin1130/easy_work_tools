#!/usr/bin/python
# -*- coding: utf-8 -*-
"""This example helps you to define arbitrary waveforms read out from a file."""

from time import sleep

from pipython import GCSDevice, pitools

CONTROLLERNAME = 'E-712'
STAGES = None  # connect stages to axes
REFMODE = None  # reference the connected stages

DATAFILE = r'wavegenerator_pnt.txt'
NUMCYLES = 1 # number of cycles for wave generator output
TABLERATE = 100  # duration of a wave table point in multiples of servo cycle times as integer
ip = '172.16.0.35'

def get_pidev(ip):
    pidevice = GCSDevice(CONTROLLERNAME)
    pidevice.ConnectTCPIP(ipaddress=ip)
    print('connected: {}'.format(pidevice.qIDN().strip()))
    print('initialize connected stages...')
    pitools.startup(pidevice, stages=STAGES, refmode=REFMODE)
    return pidevice

def pidev_genwave(pidevice, start_pos = [0, 0], end_pos = [100, 100], step_size = [0.1, 0.1]):
    length_x = round((end_pos[0] - start_pos[0]) / step_size[0])
    length_y = round((end_pos[1] - start_pos[1]) / step_size[1])
    speedup = 1
    pidevice.WAV_RAMP(table=1, firstpoint=start_pos[0] * step_size[0], numpoints=length_x * 2,
                      append='X', center=length_x, speedupdown=speedup,
                      amplitude=end_pos[0], offset=start_pos[0], seglength=length_x * 2)
    print(pidevice.qGWD(1, 1, length_x * 2))
    while pidevice.bufstate is not True:
        data = pidevice.bufdata
    tail = data[0][len(data[0]) >> 1 : ]
    data[0] = data[0] * (length_y >> 1)
    data[0] += [start_pos[0]]*len(tail)
    for i in range(len(data[0])):
        data[0][i] = 0
    tt = []
    for i in range(length_y):
        tt += [i * step_size[1] + start_pos[1]] * length_x
    tt += tail
    # wavedata = [tt, data[0]]  # readwavedata()
    wavedata = [data[0], tt]  # readwavedata()
    axes = pidevice.axes[:len(wavedata)]
    print(axes)
    assert len(wavedata) == len(axes), 'this sample requires {} connected axes'.format(len(wavedata))
    wavetables = [i for i in range(1, len(wavedata) + 1)]
    wavegens = [i for i in range(1, len(wavedata) + 1)]

    if pidevice.HasWCL():  # you can remove this code block if your controller does not support WCL()
        print('clear wave tables {}'.format(wavetables))
        pidevice.WCL(wavetables)
    for i, wavetable in enumerate(wavetables):
        print('write wave points of wave table {} and axis {}'.format(wavetable, axes[i]))
        pitools.writewavepoints(pidevice, wavetable, wavedata[i], bunchsize=10)
    if pidevice.HasWSL():  # you can remove this code block if your controller does not support WSL()
        print('connect wave tables {} to wave generators {}'.format(wavetables, wavegens))
        pidevice.WSL(wavegens, wavetables)
        print(pidevice.qWTR())
    if pidevice.HasWGC():  # you can remove this code block if your controller does not support WGC()
        print('set wave generators {} to run for {} cycles'.format(wavegens, NUMCYLES))
        pidevice.WGC(wavegens, [NUMCYLES] * len(wavegens))
    return wavegens
def pidev_prepare(pidevice, start_pos):
    axes = pidevice.axes[:len(start_pos)]
    if pidevice.HasWTR():  # you can remove this code block if your controller does not support WTR()
        print('set wave table rate to {} for wave generators {}'.format(TABLERATE, axes))
        print(pidevice.qWTR([0,1]))#qSPA(0x13000109))
        pidevice.CCL(1, 'ADVANCED')
        pidevice.SPA(1, 0x13000109, TABLERATE)
        pidevice.CCL(0)
        print(pidevice.qWTR([0, 1]))

    print('move axes {} to start positions {}'.format(axes, start_pos))
    pidevice.MOV(axes, start_pos)
    pitools.waitontarget(pidevice, axes)
    print('start wave generators for axes:{}'.format(axes))

def main():
    """Connect controller, setup wave generator, move axes to startpoint and start wave generator."""
    with GCSDevice(CONTROLLERNAME) as pidevice:
        pidevice.i(ipaddress='172.16.0.35')

        # Controllers like C-843 and E-761 are connected via PCI.
        # pidevice.ConnectPciBoard(board=1)

        # Each PI controller supports the qIDN() command which returns an
        # identification string with a trailing line feed character which
        # we "strip" away.

        print('connected: {}'.format(pidevice.qIDN().strip()))
        print('initialize connected stages...')
        pitools.startup(pidevice, stages=STAGES, refmode=REFMODE)
        pidevice, wavegens = runwavegen(pidevice)

        daq = DABoard()
        daq_ip = '172.16.0.170'
        board_status = daq.connect(daq_ip)
        update_dataaquire_reg(daq)
        trig_cnt, data_shape = DataAquire_prepare(daq)
        print(trig_cnt, data_shape)
        pidev_run(pidevice, wavegens)
        ret = DataAquire_start(daq, trig_cnt, data_shape, false_data=False)

        time.sleep(1)
        update_dataaquire_reg(daq)
        print(len(ret))
        # print(ret[0])
        # print(ret[1])
        hdf5_write('FPGA control board', ret)
        daq.disconnect()
        return ret

import matplotlib.pyplot as plt
# def runwavegen(pidevice):
#     """Read wave data, set up wave generator and run them.
#     @type pidevice : pipython.gcscommands.GCSCommands
#     """
#     step_size = 5
#     start_pos = (0, 0)
#     end_pos = (100, 100)
#     length_x = round((end_pos[0] - start_pos[0])/step_size)
#     length_y = round((end_pos[1] - start_pos[1])/step_size)
#     speedup = 1
#     pidevice.WAV_RAMP(table=1, firstpoint=start_pos[0]*step_size, numpoints=length_x * 2,
#                       append='X', center=length_x, speedupdown=speedup,
#                       amplitude=end_pos[0], offset=start_pos[0], seglength=length_x * 2)
#     print(pidevice.qGWD(1, 1, length_x * 2))
#     while pidevice.bufstate is not True:
#         data = pidevice.bufdata
#     data[0] = data[0] * (length_y >> 1)
#     tt = []
#     for i in range(length_y):
#         tt += [i*step_size+start_pos[1]] * length_x
#     # print(tt)
#     # plt.figure()
#     # plt.plot(tt)
#     # plt.show()
#
#     if pidevice.HasWTR():  # you can remove this code block if your controller does not support WTR()
#         print('set wave table rate to {} for wave generators {}'.format(TABLERATE, wavegens))
#         print(pidevice.qWTR([0,1]))#qSPA(0x13000109))
#         pidevice.CCL(1, 'ADVANCED')
#         pidevice.SPA(1, 0x13000109, TABLERATE)
#         pidevice.CCL(0)
#         print(pidevice.qWTR([0, 1]))
#
#     startpos = [wavedata[i][0] for i in range(len(wavedata))]
#     print('move axes {} to start positions {}'.format(axes, startpos))
#     pidevice.MOV(axes, startpos)
#     pitools.waitontarget(pidevice, axes)
#     print('start wave generators {}'.format(wavegens))
#     # pidevice.WGO(wavegens, mode=[1] * len(wavegens))
#     # while any(list(pidevice.IsGeneratorRunning(wavegens).values())):
#     #     print('.')
#     #     sleep(1.0)
#     # print('\nreset wave generators {}'.format(wavegens))
#     # # pidevice.WGO(wavegens, mode=[0] * len(wavegens))
#     print('E-712  prepare done')
#     return pidevice, wavegens

def pidev_run(pidevice,  start_pos):

    wavegens = [i for i in range(1, len(start_pos) + 1)]
    pidevice.WGO(wavegens, mode=[1] * len(wavegens))

def readwavedata():
    """Read DATAFILE, must have a column for each wavetable.
    @return : Datapoints as list of lists of values.
    """
    print('read wave points from file {}'.format(DATAFILE))
    data = None
    with open(DATAFILE) as datafile:
        for line in datafile:
            items = line.strip().split()
            if data is None:
                print('found {} data columns in file'.format(len(items)))
                data = [[] for _ in range(len(items))]
            for i in range(len(items)):
                data[i].append(items[i])
    return data


from DAboard import *
from data_aquire_control import *

if __name__ == '__main__':
    # import logging
    # logging.basicConfig(level=logging.DEBUG)
    ret = main()
    pos1 = ret[6]
    pos2 = ret[7]
    plt.figure()
    plt.title('axis 1 and  axis 2 postion figure, up is axis 1, down is axis 2')
    plt.subplot(211)
    plt.plot(pos1[1])
    plt.ylabel('mm')
    plt.subplot(212)
    plt.plot(pos2[1])
    plt.ylabel('mm')
    plt.xlabel('20us/sample point')
    plt.show()
