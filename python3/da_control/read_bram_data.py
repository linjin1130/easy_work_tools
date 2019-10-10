import math
import struct
import time

data_item_size = 13
def update_dataaquire_reg(da):
    '''
    :param da: da板对象
    :return: void
    notes::

        将数据获取模块寄存器寄存器值刷入状态包中
    '''
    da.Run_Command(da.board_def.CTRL_DATA_AQUIRE, 0, 0)

def start_ddr_read(da):
    '''
    :param da: da板对象
    :return: void
    notes::

        启动一次DDR数据的读取
    '''
    DataAquire_write(da, 0, 1)

def DataAquire_write(da, addr, data):
    '''
    :param da:
    :param addr: data aquire模块寄存器空间偏移地址
    :param data: data aquire模块寄存器写入数据
    :return: None
    notes::

        数据获取模块寄存器写入
        地址范围0-15，每个地址4字节数据
    '''

    data0 = addr | (1 << 8)
    # print(da.board_def.CTRL_DATA_AQUIRE, data0, data)
    da.Run_Command(da.board_def.CTRL_DATA_AQUIRE, data0, data)


def DataAquire_read(da, addr):
    '''
    :param da:
    :param addr: 寄存器偏移地址，范围（0-15）
    :return: 对应地址的寄存器数据
    notes::

        数据获取模块寄存器读取
        地址范围0-15，每个地址4字节数据
    '''

    data0 = addr | (2 << 8)
    reg_data = da.Run_Command(da.board_def.CTRL_DATA_AQUIRE, data0, 0)
    cnt = struct.unpack('I', reg_data)
    return cnt[0]

def DataAquire_readxx(da, addr):
    '''
    :param da:
    :param addr: 寄存器偏移地址，范围（0-15）
    :return: 对应地址的寄存器数据
    notes::

        数据获取模块寄存器读取
        地址范围0-15，每个地址4字节数据
    '''

    data0 = addr | (2 << 8)
    reg_data = da.Run_Command(da.board_def.CTRL_DATA_AQUIRE, data0, 0)
    cnt = struct.unpack('I', reg_data)
    return cnt[0]


def SetReadBRAM(da, flag):
    '''
    :param da:
    :param flag: 读BRAM数据标识
    :return: None
    notes::

        数据获取模块寄存器写入
        flag: 1表示当前读取BRAM数据标识使能， 0表示禁止
    '''

    data0 = (3 << 8)
    da.Run_Command(da.board_def.CTRL_DATA_AQUIRE, data0, flag)


def ReadDataAquire_Data(da, addr, length):
    '''

    :param da:
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
    SetReadBRAM(da, 1)
    data = da.Read_RAM(addr, length)
    SetReadBRAM(da, 0)
    # print(data)
    return data


def DataAnalysis(data, data_cnt):
    '''
    :param data: 待解析数据
    :param data_cnt: 待解析数据单元个数
    :return: 解析完成的数据

    notes::

        数据获取模块的数据解析,底层逻辑每收到一次触发就会产生一个数据，
        一个数据包含采样时间，PMT计数，3个pos数据以及3个pos各自数据对应的计数偏移

    底层逻辑::

        assign status_1 =  trig_lock_timing_count;
        assign status_2 =  trig_lock_pmt_count;
        assign status_3 =  trig_lock_pos_time;
        assign status_4 =  trig_lock_pos_data[31:0];
        assign status_5 =  trig_lock_pos_data[48+31:48];
        assign status_6 =  trig_lock_pos_data[96+31:96];
    '''

    with open('raw.dat', 'wb') as f:
        f.write(data)
    # 返回的数据是小端数据
    fmt = '<' + 'I8BIHIHIHIHIHIHI' * data_cnt
    item_num = 22
    anlysed_data = struct.unpack(fmt, data)

    print(f'解析数据:{len(anlysed_data)}')
    # print(anlysed_data)
    trig_lock_timing_count = ['collect time',anlysed_data[0:-1:item_num]]
    trig_lock_pos_time1 = ['positon 1 offset count',anlysed_data[1:-1:item_num]]
    trig_lock_pos_time2 = ['positon 2 offset count',anlysed_data[2:-1:item_num]]
    trig_lock_pos_time3 = ['positon 3 offset count',anlysed_data[3:-1:item_num]]
    trig_lock_pos_time4 = ['positon 4 offset count',anlysed_data[4:-1:item_num]]
    # trig_lock_pos_time5 = ['positon 5 offset count',anlysed_data[5:-1:item_num]]
    # trig_lock_pos_time6 = ['positon 6 offset count',anlysed_data[6:-1:item_num]]
    # t_low1 = anlysed_data[9:-1:item_num]
    trig_lock_pos_data_low_1 = anlysed_data[9 :-1:item_num]
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
    trig_lock_pmt_count = ['PMT counter', anlysed_data[21:-1:item_num]]
    # print(trig_lock_pos_data_up_1,trig_lock_pos_data_low_1)
    # tt = zip(trig_lock_pos_data_up_1, trig_lock_pos_data_low_1)
    # for item in tt:
    #     print(type(item[0]),item[0], print(type(item[1])), item[1])
    #     print((item[0] << 32) | item[1])
    trig_lock_pos_data1 = ['positon 1 data',
                           [(high << 32) | low for high, low in zip(trig_lock_pos_data_up_1, trig_lock_pos_data_low_1)]]
    trig_lock_pos_data2 = ['positon 2 data',
                           [(high << 32) | low for high, low in zip(trig_lock_pos_data_up_2, trig_lock_pos_data_low_2)]]
    trig_lock_pos_data3 = ['positon 3 data',
                           [(high << 32) | low for high, low in zip(trig_lock_pos_data_up_3, trig_lock_pos_data_low_3)]]
    trig_lock_pos_data4 = ['positon 4 data',
                           [(high << 32) | low for high, low in zip(trig_lock_pos_data_up_4, trig_lock_pos_data_low_4)]]
    # trig_lock_pos_data5 = ['positon 5 data',
    #                        [(high << 32) | low for high, low in zip(trig_lock_pos_data_up_5, trig_lock_pos_data_low_5)]]
    # trig_lock_pos_data6 = ['positon 6 data',
    #                        [(high << 32) | low for high, low in zip(trig_lock_pos_data_up_6, trig_lock_pos_data_low_6)]]

    return [trig_lock_timing_count, trig_lock_pmt_count, trig_lock_pos_time1, trig_lock_pos_time2,
            trig_lock_pos_time3, trig_lock_pos_time4, trig_lock_pos_data1, trig_lock_pos_data2, trig_lock_pos_data3, trig_lock_pos_data4]


def set_trig(da, trig_interval=1e-3, trig_count=10000, trig_width=1e-6):
    """
    :param da:
    :param trig_interval: 触发间隔， 单位秒, 分辨率4ns 默认1ms
    :param trig_width:  触发宽度， 单位秒, 分辨率4ns， 默认1us
    :return:
    """
    # 禁止触发
    DataAquire_write(da, 2, 0)  # 触发个数 0 表示禁止触发
    # 设置内部触发
    clock_freq = 1e8  # 时钟频率为100M
    trig_interval_cnt = int(trig_interval * clock_freq)
    trig_width_cnt = int(trig_width * clock_freq)
    DataAquire_write(da, 3, trig_interval_cnt)  # 触发间隔
    DataAquire_write(da, 4, trig_width_cnt)  # 触发宽度
    # 启动触发
    DataAquire_write(da, 2, trig_count)  # 触发个数 5000


def DataAquire_Control(da, target_data_count=10000, false_data=False):
    '''
    :param da:
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
    trig_interval = 1e-4
    trig_count = target_data_count
    trig_width = 1e-6

    DataAquire_write(da, 0, 1<<8)  # 禁止采集
    DataAquire_write(da, 5, target_data_count*data_item_size)  # 采集数据目标个数
    DataAquire_write(da, 6, 1)  # 启动采集
    if false_data:
        DataAquire_write(da, 1, 1)  # 使用假数据
        set_trig(da, trig_interval=trig_interval, trig_count=trig_count, trig_width=trig_width)
        DataAquire_write(da,0,0x80000000)

    collected_data_cnt = 0
    try_cnt = 20
    wait_time = trig_interval * trig_count / 10
    while collected_data_cnt < target_data_count and try_cnt > 0:
        time.sleep(wait_time)
        collected_data_cnt = DataAquire_read(da, 6)
        procced = collected_data_cnt / target_data_count * 100.0
        procced = round(procced, 2)
        print(f'进度：{collected_data_cnt}/{target_data_count},{procced}%')
        try_cnt -= 1
    DataAquire_write(da, 6, 0)  # 禁止采集
    if try_cnt == 0:
        return []
    raw_data = b''
    # for k in range(math.ceil(target_data_count/2000)):
    #     print(k)
    #     seg = 2000
    #     for i in range(round(2000 / seg)):
    #         raw_data += ReadDataAquire_Data(da, 2000* 24*k+seg * 24 * i, seg * 24)
    print(time.time())
    raw_data = ReadDataAquire_Data(da, 0, target_data_count * data_item_size * 4)
    print(time.time())
    # print(len(raw_data))
    # for i in range(round(target_data_count/200)):
    # print(len(raw_data[:target_data_count]))
    #     raw_data += ReadDataAquire_Data(da, 200 * 24 * i, 200 * 24)
    ret_data = DataAnalysis(raw_data[:target_data_count*data_item_size * 4], target_data_count)
    return ret_data

import datetime
import h5py  # 导入工具包
def hdf5_write(group, data):
    date_str = datetime.datetime.now().strftime("%Y%m%d%H%M")
    file_name = date_str + '.h5'
    # print(addr)

    with h5py.File(file_name, "w") as f:
        for items in data:
            path = '/'.join([group, items[0]])
            f.create_dataset(path, shape=(len(items[1]), 1), dtype='f', compression='gzip', data=items[1])

if __name__ == '__main__':
    from DAboard import *
    da = DABoard()
    new_ip = '10.0.0.170'

    board_status = da.connect(new_ip)
    update_dataaquire_reg(da)
    ret = DataAquire_Control(da, 10000, false_data=True)
    time.sleep(1)
    update_dataaquire_reg(da)
    print(len(ret))
    # print(ret[0])
    # print(ret[1])
    hdf5_write('FPGA control board', ret)
    da.disconnect()