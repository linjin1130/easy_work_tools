import time
import numpy as np
from da_board import *
from data_waves import *
import filecmp

import matplotlib.pyplot as plt
# da_list = [113, 217, 188, 226, 149, 223, 153]
# da_list = [206,186,156,200,132,12,4,2,16,28,208,213]
da_list = [206,156,12,4,2,28,213]
# da_list = [156,200,12,2,16,28,208]
# da_list = [206,186,156,200,132,12,4,2,16,28,208]
da_list += [186, 157, 149, 211, 153, 164, 154]#, 217]
# da_list += [ 158,  215,  137, 194, 144, 219, 216]
da_list += [ 158,  215, 137,  194, 144, 219, 216]

da_list = [ 158,  215, 137,  194, 144, 219, 216]
da_list += [206,156,12,4,2,16,28]
da_list += [ 157, 149, 211, 153, 164, 154]
da_list = [ 144]
# da_list = [i for i in range(80)]
# da_list = [157, 217, 188, 149, 211, 223, 153, 226, 154]
das = [DABoard(id=f'F{id}', ip=f'10.0.5.{id}', data_offset=[0,0,0,0], batch_mode=True) for id in da_list]

def init():
    for da in das:
        da.connect()
        # da.init_tcp()
        da.init_device()


da_ctrl = waveform()
# da_ctrl.generate_seq()
# da_ctrl.generate_sin(repeat=2048)
_width = 2000
da_ctrl.generate_squr(repeat=1, lowtime1=0, hightime=_width, lowtime2=_width, low=32768, high=65535, pad=1)
da_ctrl.generate_seq()
# da_ctrl.generate_trig_seq(loopcnt=1024)
# print(len(da_ctrl.seq))
# print(len(da_ctrl.wave))
# print("wave")
# da_ctrl.wave_preview()
# da_ctrl.wave = da_ctrl.wave[:20000]
# da_ctrl.seq = da_ctrl.seq[:32]
da_ctrl.wave = np.asarray(da_ctrl.wave, dtype='<u2')
da_ctrl.seq = np.asarray(da_ctrl.seq, dtype='<u2')
# c = da_ctrl.seq.tobytes()
print(len(da_ctrl.wave))
print(len(da_ctrl.seq))

_start = time.time()
# cycle_cnt = 10000

def run_non_blocking(das, batch_mode):
    for da in das:
        da.batch_mode = batch_mode
    _start = time.time()
    cycle_cnt = 10
    t = {'1 write wave':[], '2 commit wave':[], '3 waite wave response':[],
         '4 write cmd':[], '5 commit cmd':[], '6 waite cmd response':[],'7 send trig':[]}
    ts = [0]*8
    for i in range(cycle_cnt):
        ts[0] = time.time()
        for da in das:
            for ch in range(4):
                # da.write_seq(ch+1,seq=da_ctrl.seq)
                # da.write_wave(ch+1,wave=da_ctrl.wave)
                da.write_seq_fast(ch+1,seq=da_ctrl.seq)
                da.write_wave_fast(ch+1,wave=da_ctrl.wave)
        ts[1] = time.time()
        if batch_mode:
            for da in das:\
                # da.commit_mem()
                da.commit_mem_fast()
        ts[2] = time.time()
        if batch_mode:
            for da in das:
                da.wait_response()
        ts[3] = time.time()
        for da in das:
            da.stop_output_wave(0)
            da.set_trig_count_l1(60000)
            da.set_trig_interval_l1(200e-6)
            da.start_output_wave(1)
            da.start_output_wave(2)
            da.start_output_wave(3)
            da.start_output_wave(4)
        ts[4] = time.time()
        if batch_mode:
            for da in das:
                da.commit_para()
        ts[5] = time.time()
        if batch_mode:
            for da in das:
                da.wait_response()
        ts[6] = time.time()
        das[0].send_int_trig()
        ts[7] = time.time()
        for idx, key in enumerate(t.keys()):
            t[key].append(ts[idx+1]-ts[idx])
    _stop = time.time()
    print(f'board counts: {len(das)}, cycle count: {cycle_cnt}, time is: {round(_stop-_start, 5)}s')
    return t

def run(batch_mode):
    all_t = []
    for num in range(1,len(das)+1):
        t = run_non_blocking(das[0:num], batch_mode)
        all_t.append(t)
    return all_t

from numpy import *
def process(all_t):
    _t = {'1 write wave':[], '2 commit wave':[], '3 waite wave response':[],
             '4 write cmd':[], '5 commit cmd':[], '6 waite cmd response':[],
          '7 send trig':[], '8 total': [], '9 totoal without write wave':[]}
    for t in all_t:
        _total = 0
        for key in t.keys():
            avg = mean(t[key])
            _t[key].append(avg)
            _total += avg
        _t['8 total'].append(_total)
        _t[ '9 totoal without write wave'].append(_total-_t['1 write wave'][-1])
    return _t

import matplotlib.pyplot as plt
def draw(_t, batch_mode):
    '''ref: https://blog.csdn.net/Poul_henry/article/details/82533569'''
    plt.figure(f'时间消耗测试batch mode-{batch_mode}')
    # plt.title(f'time consuming test, with batch mode:{batch_mode}')
    ax1 = plt.subplot()
    for key in _t.keys():
        ax1.plot(_t[key], label=key)
    plt.xlabel(f'awg board number\n time consuming test, with batch mode:{batch_mode}')
    plt.ylabel('time consumed(seconds)')
    box = ax1.get_position()
    ax1.set_position([box.x0, box.y0, box.width, box.height*0.8])
    ax1.legend(loc='center left', bbox_to_anchor=(0.05, 1.2), ncol=2)

    # plt.legend(loc='BestOutside')
    # plt.legend()
    plt.show()
    time.sleep(2)
    plt.close()

def test(batch_mode):
    all_t = run(batch_mode)
    _t = process(all_t)
    # draw(_t, batch_mode)

for i in range(1):
    init()
    test(batch_mode=True)
    print(f'当前测试轮数：{i}')