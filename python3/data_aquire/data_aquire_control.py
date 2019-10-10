import math
import struct
import time
from functools import reduce

import matplotlib.pyplot as plt
import numpy as np

data_item_size = 13


np.random.seed(19680801)
data = np.random.random((100, 100, 100))


def update_dataaquire_reg(daq):
    '''
    :param daq: da板对象
    :return: void
    notes::

        将数据获取模块寄存器寄存器值刷入状态包中
    '''
    daq.Run_Command(daq.board_def.CTRL_DATA_AQUIRE, 0, 0)


def start_ddr_read(daq):
    '''
    :param daq: da板对象
    :return: void
    notes::

        启动一次DDR数据的读取
    '''
    DataAquire_write(daq, 0, 1)


def DataAquire_write(daq, addr, data):
    '''
    :param daq:
    :param addr: data aquire模块寄存器空间偏移地址
    :param data: data aquire模块寄存器写入数据
    :return: None
    notes::

        数据获取模块寄存器写入
        地址范围0-15，每个地址4字节数据
    '''

    data0 = addr | (1 << 8)
    # print(daq.board_def.CTRL_DATA_AQUIRE, data0, data)
    daq.Run_Command(daq.board_def.CTRL_DATA_AQUIRE, data0, data)


def DataAquire_read(daq, addr):
    '''
    :param daq:
    :param addr: 寄存器偏移地址，范围（0-15）
    :return: 对应地址的寄存器数据
    notes::

        数据获取模块寄存器读取
        地址范围0-15，每个地址4字节数据
    '''

    data0 = addr | (2 << 8)
    reg_data = daq.Run_Command(daq.board_def.CTRL_DATA_AQUIRE, data0, 0)
    cnt = struct.unpack('I', reg_data)
    return cnt[0]

def DataAquire_dac_write(daq, data):
    '''
    :param daq:
    :param data: dac 数据， 24比特
    :return:
    notes::
    '''

    DataAquire_write(daq, 10, data)
    DataAquire_write(daq, 0, 1<<1)

def DataAquire_readxx(daq, addr):
    '''
    :param daq:
    :param addr: 寄存器偏移地址，范围（0-15）
    :return: 对应地址的寄存器数据
    notes::

        数据获取模块寄存器读取
        地址范围0-15，每个地址4字节数据
    '''

    data0 = addr | (2 << 8)
    reg_data = daq.Run_Command(daq.board_def.CTRL_DATA_AQUIRE, data0, 0)
    cnt = struct.unpack('I', reg_data)
    return cnt[0]


def SetReadBRAM(daq, flag):
    '''
    :param daq:
    :param flag: 读BRAM数据标识
    :return: None
    notes::

        数据获取模块寄存器写入
        flag: 1表示当前读取BRAM数据标识使能， 0表示禁止
    '''

    data0 = (3 << 8)
    daq.Run_Command(daq.board_def.CTRL_DATA_AQUIRE, data0, flag)


def ReadDataAquire_Data(daq, addr, length):
    '''

    :param daq:
    :param addr: 读取数据的起始地址，一般为0
    :param length: 读取数据的字节数
    :return: data in string bytes
    notes::

        读取数据获取模块采集的数据
        数据获取模块存储空间最大1MB
        所以地址和长度不能超过这个限制
        读取这个数据前，首先要设置当前读取BRAM标识使能
        然后才能读数据
    '''
    # SetReadBRAM(daq, 1)
    assert addr+length < 0x40000000
    data = daq.Read_RAM(addr, length)
    # SetReadBRAM(daq, 0)
    # print(data)
    return data


def DataAnalysis(analysed_data, data):
    '''
    :param analysed_data: 已解析数据
    :param data: 待解析数据
    :return:

    notes::

        数据获取模块的数据解析,底层逻辑每收到一次触发就会产生一个数据，
        一个数据包含采样时间，PMT计数，6个pos数据以及6个pos各自数据对应的计数偏移

    底层逻辑::

        assign status_1 =  trig_lock_timing_count;
        assign status_2 =  trig_lock_pmt_count;
        assign status_3 =  trig_lock_pos_time;
        assign status_4 =  trig_lock_pos_data[31:0];
        assign status_5 =  trig_lock_pos_data[48+31:48];
        assign status_6 =  trig_lock_pos_data[96+31:96];
    '''

    # data_cnt: 待解析数据单元个数
    data_cnt = round(len(data)/(data_item_size*4))

    # with open('raw.dat', 'wb') as f:
    #     f.write(data)
    # 返回的数据是小端数据
    fmt = '<' + 'I8BIHIHIHIHIHIHI' * data_cnt
    item_num = 22
    anlysed_data = struct.unpack(fmt, data)

    # print(f'解析数据个数:{data_cnt}')
    # print(anlysed_data)
    trig_lock_timing_count = ['collect time', anlysed_data[0:-1:item_num]]
    trig_lock_pos_time1 = ['positon 1 offset count', anlysed_data[1:-1:item_num]]
    trig_lock_pos_time2 = ['positon 2 offset count', anlysed_data[2:-1:item_num]]
    trig_lock_pos_time3 = ['positon 3 offset count', anlysed_data[3:-1:item_num]]
    trig_lock_pos_time4 = ['positon 4 offset count', anlysed_data[4:-1:item_num]]
    # trig_lock_pos_time5 = ['positon 5 offset count',anlysed_data[5:-1:item_num]]
    # trig_lock_pos_time6 = ['positon 6 offset count',anlysed_data[6:-1:item_num]]
    # t_low1 = anlysed_data[9:-1:item_num]
    trig_lock_pos_data_low_1 = anlysed_data[9:-1:item_num]
    trig_lock_pos_data_low_2 = anlysed_data[11:-1:item_num]
    trig_lock_pos_data_low_3 = anlysed_data[13:-1:item_num]
    trig_lock_pos_data_low_4 = anlysed_data[15:-1:item_num]
    # trig_lock_pos_data_low_5 = anlysed_data[17:-1:item_num]
    # trig_lock_pos_data_low_6 = anlysed_data[19:-1:item_num]
    trig_lock_pos_data_up_1 = anlysed_data[10:-1:item_num]
    trig_lock_pos_data_up_2 = anlysed_data[12:-1:item_num]
    trig_lock_pos_data_up_3 = anlysed_data[14:-1:item_num]
    trig_lock_pos_data_up_4 = anlysed_data[16:-1:item_num]
    # trig_lock_pos_data_up_5 = anlysed_data[18:-1:item_num]
    # trig_lock_pos_data_up_6 = anlysed_data[20:-1:item_num]
    trig_lock_pmt_count = ['PMT counter', anlysed_data[21::item_num]]
    # print(trig_lock_pos_data_up_1,trig_lock_pos_data_low_1)
    # tt = zip(trig_lock_pos_data_up_1, trig_lock_pos_data_low_1)
    # for item in tt:
    #     print(type(item[0]),item[0], print(type(item[1])), item[1])
    #     print((item[0] << 32) | item[1])
    trig_lock_pos_data1 = ['positon 1 data',
                           [((high << 32) | low) / 1e9  for high, low in zip(trig_lock_pos_data_up_1, trig_lock_pos_data_low_1)]]
    trig_lock_pos_data2 = ['positon 2 data',
                           [((high << 32) | low) / 1e9 for high, low in zip(trig_lock_pos_data_up_2, trig_lock_pos_data_low_2)]]
    trig_lock_pos_data3 = ['positon 3 data',
                           [((high << 32) | low) / 1e9 for high, low in zip(trig_lock_pos_data_up_3, trig_lock_pos_data_low_3)]]
    trig_lock_pos_data4 = ['positon 4 data',
                           [((high << 32) | low) / 1e9 for high, low in zip(trig_lock_pos_data_up_4, trig_lock_pos_data_low_4)]]
    # trig_lock_pos_data5 = ['positon 5 data',
    #                        [(high << 32) | low for high, low in zip(trig_lock_pos_data_up_5, trig_lock_pos_data_low_5)]]
    # trig_lock_pos_data6 = ['positon 6 data',
    #                        [(high << 32) | low for high, low in zip(trig_lock_pos_data_up_6, trig_lock_pos_data_low_6)]]
    temp = [trig_lock_timing_count, trig_lock_pmt_count, trig_lock_pos_time1, trig_lock_pos_time2,
            trig_lock_pos_time3, trig_lock_pos_time4, trig_lock_pos_data1, trig_lock_pos_data2, trig_lock_pos_data3,
            trig_lock_pos_data4]
    new_analysed_data = temp

    if analysed_data == None:
        new_analysed_data = temp
    else:
        for idx in range(len(temp)):
            new_analysed_data[idx][1] = analysed_data[idx][1] + temp[idx][1]
            # print(new_analysed_data[idx][0],len(new_analysed_data[idx][1]))
    return temp, new_analysed_data


def set_trig(daq, trig_interval=1e-3, trig_count=10000, trig_width=1e-6):
    """
    :param daq:
    :param trig_interval: 触发间隔， 单位秒, 分辨率4ns 默认1ms
    :param trig_width:  触发宽度， 单位秒, 分辨率4ns， 默认1us
    :return:
    """

    # 设置内部触发
    print(f'触发参数:trig:count{trig_count}')
    clock_freq = 1e8  # 时钟频率为100M
    trig_interval_cnt = int(trig_interval * clock_freq)
    trig_width_cnt = int(trig_width * clock_freq)
    DataAquire_write(daq, 3, trig_interval_cnt)  # 触发间隔
    DataAquire_write(daq, 4, trig_width_cnt)  # 触发宽度
    DataAquire_write(daq, 2, trig_count)  # 触发个数

def DataAquire_prepare(daq, data_cnt = 10000):
    trig_count = 1
    trig_interval = 1e-6
    trig_width = 1e-7

    set_trig(daq, trig_interval=trig_interval, trig_count=trig_count, trig_width=trig_width)

    target_data_count = data_cnt
    DataAquire_write(daq, 6, 0)  # 禁止采集, fifo 清空
    DataAquire_write(daq, 0, 1 << 8)  # 禁止采集, fifo 清空
    DataAquire_write(daq, 1, 0)  # 使用真实数据
    DataAquire_write(daq, 5, target_data_count)  # 采集数据字数，每个4字节
    DataAquire_write(daq, 6, 1)  # 使能采集

def draw_fig(data):
    # plt.clf()  # 清除之前画的图
    plt.imshow(data)  # 画出当前 ax 列表和 ay 列表中的值的图形
    plt.pause(0.001)  # 暂停一秒

def DataAquire_start(daq, size_shape=10000, false_data=False):
    '''
    :param daq:
    :param taget_data_count: 待采集的数据个数
    :return: 返回采集的数据，如果失败，返回空列表
    notes::

        数据采集控制过程：
        1. 重置采集参数
        2. 数据采集使能
        3. 读取采集个数
        4. 读取数据，等待完成或超时
        5. 处理数据
        6. 返回

    '''

    if false_data:
        DataAquire_write(daq, 1, 0)  # 使用假数据
    # 启动采集
    DataAquire_write(daq, 0, 0x80000000)

    collected_data_cnt = 0 # 已生成的数据个数

    # 等待采集完成
    while collected_data_cnt < size_shape:
        collected_data_cnt = DataAquire_read(daq, 6)
        # print(collected_data_cnt)
    # 读取采集数据
    start_addr = 0
    data_size = size_shape << 2
    temp_data = ReadDataAquire_Data(daq, start_addr, data_size)

    return temp_data


import datetime
import h5py  # 导入工具包


def hdf5_write(group, data):
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    file_name = 'data/'+date_str + '.h5'
    # file_name = date_str + '.h5'
    # print(addr)

    with h5py.File(file_name, "w") as f:
        for items in data:
            path = '/'.join([group, items[0]])
            f.create_dataset(path, shape=(len(items[1]), 1), dtype='f', compression='gzip', data=items[1])

# def draw_fig(data_in=[None]*10):
#     # l = len(data)
#     pos1 = data_in[6]
#     pos2 = data_in[7]
#     plt.figure()
#     plt.subplot(211)
#     plt.plot(pos1[1])
#     plt.subplot(212)
#     plt.plot(pos2[1])
#     plt.show()

if __name__ == '__main__':
    from DAboard import *

    daq = DABoard()
    new_ip = '172.16.0.170'

    board_status = daq.connect(new_ip)
    update_dataaquire_reg(daq)
    trig_cnt, data_shape = DataAquire_prepare(daq)
    print(trig_cnt, data_shape)
    ret = DataAquire_start(daq, trig_cnt, data_shape, false_data=True)
    time.sleep(1)
    update_dataaquire_reg(daq)
    print(len(ret))
    # print(ret[0])
    # print(ret[1])
    hdf5_write('FPGA control board', ret)
    daq.disconnect()
    # draw_fig(ret)

    pos1 = ret[6]
    pos2 = ret[7]
    pos3 = [i+j for i,j in zip(pos1[1],pos2[1])]
    plt.figure()
    plt.title('axis 1 and  axis 2 postion figure, up is axis 1, down is axis 2')
    plt.subplot(311)
    plt.plot(pos1[1])
    plt.ylabel('mm')
    plt.subplot(312)
    plt.plot(pos2[1])
    plt.ylabel('mm')
    plt.subplot(313)
    plt.plot(pos3)
    plt.ylabel('mm')
    plt.xlabel('20us/sample point')
    plt.show()