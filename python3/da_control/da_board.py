# -- coding: utf-8 --
import ctypes
import time
# from numpy import clip
from numba import jit
import numpy as np
import math
from logging_util import logger

import struct
import socket

def get_host_ip():
    addrs = socket.getaddrinfo(socket.gethostname(), None)
    for item in addrs:
        if item[-1][0].find('10.0') > -1:
            return item[-1][0]
    return '10.0.255.255'

class VirtualDll:
    def __init__(self, da_id):
        self.da_id = da_id

    def __getattr__(self, name):
        def func(*args, **kargs):
            # print(f'[{self.da_id}] call dll function: {name}')
            return 0
        return func

#   函数类型抽象
class FuncType(object):
    def __init__(self, func_type, ins, para1, para2, desc):
        self.func_type = func_type
        self.ins = ins
        self.para1 = para1
        self.para2 = para2
        self.desc = desc


#   返回结果抽象
class RetResult(object):
    OK = 0
    ERROR = 1

    def __init__(self, resp_stat, resp_data, data):
        self.resp_stat = resp_stat
        self.resp_data = resp_data
        self.data = data


#   DA板的抽象
#   调用DA板驱动进行设备操作、DA板参数配置、DA通道参数配置

def format_data(data_in):
    length = len(data_in)
    data = [0 for x in range(0, length)]
    for i in range(0, length):
        data[i] = data_in[i]
    if not ((divmod(length, 32))[1] == 0):  # 补齐32bit
        length = int((math.floor(length / 32) + 1) * 32)
        data = [0 for x in range(0, length)]
        temp_len = len(data_in)
        for i in range(0, temp_len):
            data[i] = data_in[i]
    # for i in range(0, int(length / 2 - 1)):  # 颠倒数据
    #     temp = data[2 * i]
    #     data[2 * i] = data[2 * i + 1]
    #     data[2 * i + 1] = temp
    return data

class RawBoard(object):
    def __init__(self):
        self.id = None
        self.connect_status = 0
        self.ip = '127.0.0.1'
        self.port = 80
        self.timeout = 1
        self.para_addr_list = []
        self.para_data_list = []
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockfd.settimeout(self.timeout)

    def connect(self):
        """Connect to Server"""
        count = 5
        while count > 0:
            try:
                if self.sockfd is None:
                    self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    self.sockfd.settimeout(self.timeout)
                self.sockfd.connect((self.ip, self.port))
                print(f'{self.ip} connect sucessful.')
                # print(f'sock_fd, {self.sockfd}')
                self.connect_status = 1
                # self.write_command(0xdeadbeef, 0, 0, donot_ret=True)
                # init_cmd = struct.pack('I', 0xDEADBEAF)
                # self.sockfd.send(init_cmd)
                return 0
            except :
                self.connect_status = 0
                self.sockfd.close()
                self.sockfd = None
            count -= 1
            logger.info("DAC {} connect {} failed" .format(self.id, 5-count))
        if self.sockfd is None:
            logger.error("DAC %s connect failed!", self.id)
            return 1

    def disconnect(self):
        """Close the connection to the server."""
        if self.connect_status == 1:
            self.connect_status = 0
            self.sockfd.close()
            self.sockfd = None
        else:
            logger.error("DAC %s already disconnected!", self.id)
        return 0

    def Write_Reg(self, bank, addr, data):
        """Write to register command."""
        cmd = 0x02
        #I need to pack bank into 4 bytes and then only use the 3
        packedBank = struct.pack("l", bank)
        unpackedBank = struct.unpack('4b', packedBank)

        packet = struct.pack("4bLL", cmd, unpackedBank[0], unpackedBank[1], unpackedBank[2], addr, data)
    #     print ('this is my packet: {}'.format(repr(packet)))
        #Next I need to send the command
        try:
            self.send_data(packet)
        except socket.timeout:
            print (f"Write_Reg send data Timeout raised and caught: {self.id}")
        #next read from the socket
        try:
            stat, data = self.receive_data()
        except socket.timeout:
            print (f"Write_Reg recieve data Timeout raised and caught: {self.id}")
        if stat != 0x0:
            print (f'{self.id} Write_Reg Issue with Write Command stat: {stat}')
            return -1

        return 0

    def Read_Reg(self, bank, addr, data=0xFAFAFAFA):
        """Read from register command."""
        # data is used for spi write
        cmd = 0x01

        #I need to pack bank into 4 bytes and then only use the 3
        packedBank = struct.pack("l", bank)
        unpackedBank = struct.unpack('4b', packedBank)

        packet = struct.pack("4bLi", cmd, unpackedBank[0], unpackedBank[1], unpackedBank[2], addr, data)
        #Next I need to send the command
        try:
            self.send_data(packet)
        except socket.timeout:
            print (f"Read_Reg send data Timeout raised and caught: {self.id}")
        #next read from the socket
        try:
            stat, data = self.receive_data()
        except socket.timeout:
            print (f"Read_Reg recieve data Timeout raised and caught: {self.id}")

        if stat != 0x0:
            print (f'{self.id} Read_Reg Issue with Write Command stat: {stat}')
            return -1
        return data

    def read_memory(self, addr, length):
        """Read from RAM command."""
        cmd = 3
        pad = 0xFAFAFA

        #I need to pack bank into 4 bytes and then only use the 3
        packedPad = struct.pack("l", pad)
        unpackedPad = struct.unpack('4b', packedPad)

        packet = struct.pack("4bLL", cmd, unpackedPad[0], unpackedPad[1], unpackedPad[2], addr, length)
        #Next I need to send the command
        self.send_data(packet)
        #next read from the socket
        recv_stat, _ = self.receive_data()
        if recv_stat != 0x0:
            print (f'{self.id}: read_memory Issue with Reading RAM stat: {recv_stat}')
            return recv_stat
        ram_data = self.receive_RAM(int(length))
        return ram_data

    def write_memory(self, start_addr, wave):
        """Write to RAM command."""
        count = 5
        while count > 0:
            cmd = 0x04
            pad = 0xFFFFFF
            #I need to pack bank into 4 bytes and then only use the 3
            packedPad = struct.pack("L", pad)
            unpackedPad = struct.unpack('4b', packedPad)
            length = len(wave) << 1 #short 2 byte
            packet = struct.pack("4bLL", cmd, unpackedPad[0], unpackedPad[1], unpackedPad[2], start_addr, length)
            #Next I need to send the command
            self.send_data(packet)
            #next read from the socket
            recv_stat, _ = self.receive_data()
            if recv_stat != 0x0:
                print (f'{self.id} write_memory send cmd Error stat={recv_stat}!!!')
                return recv_stat
            #method 1
            format = "{0:d}H".format(len(wave))
            packet = struct.pack(format, *wave)
            self.send_data(packet)
            #next read from the socket to ensure no errors occur
            recv_stat, recv_data = self.receive_data()
            if recv_stat == -1 and recv_data == -1:
                self.disconnect()
                self.connect()
                count -= 1
                continue
        # print(packet)
            if recv_stat != 0x0:
                print (f'{self.id} write_memory send data Error stat={recv_stat}!!!')
                return recv_stat
            return 0
        return 1

    def write_command(self, ctrl, data0, data1):
        """write command."""
        # cmd = 0x05
        # packedCtrl = struct.pack("l", ctrl)
        # unpackedCtrl = struct.unpack('4b', packedCtrl)
        # packet = struct.pack("4bLL", cmd, unpackedCtrl[0], unpackedCtrl[1], unpackedCtrl[2], data0, data1)
        packet = struct.pack("LLL", ctrl, data0, data1)
    #    print ('this is my cmd packet: {}'.format(repr(packet)))
        self.send_data(packet)
        stat, data = self.receive_data()
        if stat != 0x0:
            print (f'{self.id}: write_command Error, cmd: 0x{hex(ctrl)}, error stat={stat}!')
        return stat

    def set_para(self, bank, addr, data=0):
        self.para_addr_list.append((bank << 16) | addr)
        self.para_data_list.append(data)
        # print(hex(self.para_addr_list[-1]), hex(self.para_data_list[-1]))
        assert len(self.para_addr_list) <= 128

    def wait_response(self):
        stat, data = self.receive_data()
        return stat
        
    def commit_para(self):
        cmd_cnt = len(self.para_data_list)
        msg = struct.pack('BBBB', 0x06, 0, 0, cmd_cnt)
        for addr, data in zip(self.para_addr_list, self.para_data_list):
            # print(addr, data)
            msg = msg + struct.pack('LL', addr, data)
        try:
            self.send_data(msg)
        except socket.timeout:
            print (f"Write_Reg send data Timeout raised and caught: {self.id}")
        self.para_addr_list.clear()
        self.para_data_list.clear()
        # print('commit')

    def send_data(self, msg):
        """Send data over the socket."""
        totalsent = 0
        sent = 0
        while totalsent < len(msg):
            try:
                sent = self.sockfd.send(msg)
            except:
                self.disconnect()
                break
            # if sent == 0:
            #     raise RuntimeError("Socket connection broken")
            totalsent = totalsent + sent

    def receive_data(self):
        """Read received data from the socket."""
        chunks = []
        bytes_recd = 0
        try:
            while bytes_recd < 8:
                #I'm reading my data in byte chunks
                chunk = self.sockfd.recv(min(8 - bytes_recd, 4))
                if chunk == '':
                   raise RuntimeError("Socket connection broken")
                chunks.append(chunk)
                bytes_recd = bytes_recd + len(chunk)
        except:
            raise RuntimeError("Socket connection broken")
            return -1, -1
        stat_tuple = struct.unpack('L', chunks[0])
        data_tuple = struct.unpack('L', chunks[1])

        stat = stat_tuple[0]
        data = data_tuple[0]
        # print('00000000000000', stat, data)
        return stat, data

    def receive_RAM(self, length):
        """Read received data from the socket after a read RAM command."""
        # chunks = []
        ram_data = b''
        bytes_recd = 0
        # self.sockfd.settimeout(self.timeout)
        while bytes_recd < length:
            #I'm reading my data in byte chunks
            chunk = self.sockfd.recv(min(length - bytes_recd, 1024))
            #Unpack the received data
            # data = struct.unpack("L", chunk)
            # print(type(chunk))
            ram_data += chunk
            if chunk == '':
               raise RuntimeError("Socket connection broken")
            # chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        # print(bytes_recd)
        #  print ('Print something I can understand: {}'.format(repr(chunks)))
        #  print ram_data
        return ram_data

class DABoard(RawBoard):
    #   加载DA板驱动动态库
    # dll = ctypes.cdll.LoadLibrary('USTCDACDriver.dll')
    is_block = 0  # is run in a block mode
    channel_amount = 4  # DA板通道个数，依次为X、Y、DC、Z
    def __init__(self, id="E08", ip="10.0.4.8", port=80, connect_status=0,trig_interval_l1=200e-6,trig_interval_l2=0.001,
                 trig_count_l1=10,trig_count_l2=1, output_delay=0, channel_gain=None,
                channel_default_voltage=None, data_offset=None, trig_out_delay_step=None,
                 output_delay_step=None, sample_rate=0.5e-9, sync_delay=None, batch_mode=True):
        super(DABoard, self).__init__()
        if channel_gain is None:
            channel_gain = [511 for x in range(0, self.channel_amount)]
        # if channel_offset is None:
        #     channel_offset = [0 for x in range(0, self.channel_amount)]

        if channel_default_voltage is None:
            channel_default_voltage = [32768 for x in range(0, self.channel_amount)]
        if data_offset is None:
            data_offset = [32768 for x in range(0, self.channel_amount)]
        if trig_out_delay_step is None:
            trig_out_delay_step = [4 for x in range(0, self.channel_amount)]
        if output_delay_step is None:
            output_delay_step = [4 for x in range(0, self.channel_amount)]
        if sync_delay is None:
            sync_delay = [0 for x in range(0, self.channel_amount)]
        #赋值
        self.host_ip = get_host_ip()
        self.id = id  # DA板配置表标识
        self.ip = ip.encode()  # DA板IP
        self.port = port  # DA板端口号
        self.connect_status = connect_status  # DA板连接状态
        self.batch_mode = batch_mode
        self.waves = [None]*4
        self.seqs = [None] * 4

        self.f_id = 0  # DA板文件句柄

        self.da_trig_delay_offset = 0  # DA板触发延时偏置
        self.channel_voltage_offset = [0 for x in range(0, self.channel_amount)]  # voltage offset
        #记录数据库中需初始化的信息
        self.channel_gain_info = channel_gain
        self.channel_default_voltage_info = channel_default_voltage
        self.trig_interval_l1_info = trig_interval_l1  # DA板默认触发间隔
        self.trig_interval_l2_info = trig_interval_l2  # DA板默认触发间隔
        self.trig_count_l1_info = trig_count_l1
        self.trig_count_l2_info = trig_count_l2
        self.output_delay_info = output_delay  # DA板输出延时
        # self.channel_offset = channel_offset  # DAC channel offset
        self.data_offset = data_offset
        self.trig_out_delay_step = trig_out_delay_step
        self.output_delay_step = output_delay_step
        self.sample_rate = sample_rate
        self.sync_delay = sync_delay  # DA板同步延时
        # 记录配置到板子的信息
        self.channel_gain = [None for x in range(0, self.channel_amount)]
        self.channel_default_voltage = [None for x in range(0, self.channel_amount)]
        self.trig_interval_l1 = None  # DA板默认触发间隔
        self.trig_interval_l2 = None # DA板默认触发间隔
        self.trig_count_l1 = None
        self.trig_count_l2 = None
        self.trig_delay = None  # DA板触发延时
        self.trig_delay_width=None
        self.output_delay = None  # DA板输出延时
        # if self.is_mock:
        #     self.dll = VirtualDll(self.id)
    @property
    def is_mock(self):
        return 'mock' in self.id.lower()

    def block(self):
        if self.is_block == 1:
            self.get_return(1)

    # def connect(self):
    #     # dll_func = self.dll.Open
    #     # self.f_id = ctypes.c_int(0)
    #     # ret = dll_func(ctypes.byref(self.f_id), self.ip, self.port)
    #     ret = self.raw_connect()
    #     if ret == 0:
    #         self.connect_status = 1
    #     else:
    #         self.disp_error(ret)
    #         logger.error("DAC %s connect failed!", self.id)
    #     return ret

    # def disconnect(self):
    #     ret = 0
    #     if self.connect_status == 1:
    #         dll_func = self.dll.Close
    #         ret = dll_func(self.f_id, self.ip, self.port)
    #         if ret == 0:
    #             self.connect_status = 0
    #         else:
    #             self.disp_error(ret)
    #             logger.error("DAC %s disconnect failed!", self.id)
    #     else:
    #         logger.error("DAC %s already disconnected!", self.id)
    #     return ret

    # #   写命令，DA板原子操作
    # def write_command(self, ins, para1, para2):
    #     self.connect()
    #     dll_func = self.dll.WriteInstruction
    #     ret = dll_func(self.f_id, ins, para1, para2)
    #     if not ret == 0:
    #         self.disp_error(ret)
    #     self.block()
    #     return ret

    # #   写内存数据
    # def write_memory(self, ins, start, length, data):
    #     self.connect()
    #     PData = ctypes.c_int16 * len(data)
    #     p_data = PData()
    #     p_data[:] = data  # data should be array of integers
    #     dll_func = self.dll.WriteMemory
    #     ret = dll_func(self.f_id, ins, start, length, p_data)
    #     if not ret == 0:
    #         self.disp_error(ret)
    #     self.block()
    #     return ret

    # #   读内存数据
    # def read_memory(self, ins, start, length):
    #     self.connect()
    #     dll_func = self.dll.ReadMemory
    #     ret = dll_func(self.f_id, ins, start, length)
    #     if not ret == 0:
    #         self.disp_error(ret)
    #     self.block()
    #     return ret

    # #   写寄存器
    # def write_reg(self, bank, addr, data):
    #     self.connect()
    #     cmd = bank * 256 + 2  # 表示WriteReg，指令和bank存储在一个DWORD数据中
    #     ret = self.write_command(cmd, addr, data)
    #     if not ret == 0:
    #         self.disp_error(ret)
    #         logger.error("DAC %s write reg failed!", self.id)
    #     self.block()
    #     return ret

    # #   读寄存器
    # def read_reg(self, bank, addr):
    #     self.connect()
    #     cmd = bank * 256 + 1  # 表示ReadReg，指令和bank存储在一个DWORD数据中
    #     ret, data = self.write_command(cmd, addr, 0)
    #     if not ret == 0:
    #         self.disp_error(ret)
    #         logger.error("DAC %s read reg failed!", self.id)
    #     result = self.get_return(1)
    #     return result.resp_data
    def commit_mem(self):
        cmd = [0x07, 1, 2, 3]
        packet = b''
        for wave, seq in zip(self.waves, self.seqs):
            if wave is None:
                cmd.append(0)
                cmd.append(0)
                cmd.append(0)
                cmd.append(0)
            else:
                # print(len(wave), len(seq))
                cmd.append(0)
                cmd.append(len(wave) << 1)
                packet += struct.pack(f'{len(wave)}H', *wave)
                cmd.append(0)
                cmd.append(len(seq) << 1)
                packet += struct.pack(f'{len(seq)}H', *seq)

        format = "4B16I"
        _head = struct.pack(format, *cmd)
        packet = _head + packet
        # print(f'packet len {len(packet)}')
        self.send_data(packet)
        # sta = self.fast_write_memory(packet)
        # print(f'write status: {sta}')
        self.waves = [None]*4
        self.seqs = [None]*4
    def commit_mem_fast(self):
        cmd = [0x07, 1, 2, 3]
        packet = b''
        for wave, seq in zip(self.waves, self.seqs):
            if wave is None:
                cmd.append(0)
                cmd.append(0)
                cmd.append(0)
                cmd.append(0)
            else:
                # print(len(wave), len(seq))
                # print(type(wave), type(seq))
                cmd.append(0)
                cmd.append(len(wave) << 0)
                packet += wave #struct.pack(f'{len(wave)}H', *wave)
                cmd.append(0)
                cmd.append(len(seq) << 0)
                packet += seq #struct.pack(f'{len(seq)}H', *seq)

        format = "4B16I"
        _head = struct.pack(format, *cmd)
        # print(type(_head))
        packet = _head + packet
        # print(f'packet len {len(packet)}')
        self.send_data(packet)
        # sta = self.fast_write_memory(packet)
        # print(f'write status: {sta}')
        self.waves = [None]*4
        self.seqs = [None]*4
    #不要改动
    #   写波形
    # @jit
    def wave_calc(self, channel, offset=0, wave=None):
        data_offset = self.data_offset[channel - 1] + 32768
        data = np.pad(wave, [0, 32 - (len(wave) & 31)], 'constant') + data_offset
        data = np.clip(data.astype('i'), 0, 65535).tolist()
        return data

    def wave_calc_fast(self, channel, offset=0, wave=None):
        data_offset = self.data_offset[channel - 1] + 32768
        return wave + data_offset
        #         # data = np.pad(wave, [0, 32 - (len(wave) & 31)], 'constant') + data_offset
        #         # data = np.clip(data.astype('i'), 0, 65535).tolist()
        #         # return data

    def write_wave(self, channel, offset=0, wave=None):
        if channel < 1 or channel > self.channel_amount:
            logger.error(f"[{self.id}] wrong channel: {channel}")
            return 3
        
        # data = wave + [0] * (32 - (len(wave) & 31)) #补齐32个采样点
        # data = [int(d + self.data_offset[channel - 1] + 32768) for d in data]
        # data = np.clip(data, 0, 65535).tolist()
        
        data = self.wave_calc(channel, offset, wave)

        start_addr = ((channel - 1) << 19) + 2 * offset
        if self.batch_mode:
            self.waves[channel-1] = data
            return 0
            # ret = self.fast_write_memory(start_addr, data)
        else:
            ret = self.write_memory(start_addr, data)
        # length = len(data) * 2
        # ret = self.write_memory(0x00000004, start_addr, length, data)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s write wave failed, return is: %d!", self.id, ret)
        return ret

    def write_wave_fast(self, channel, offset=0, wave=None):
        if channel < 1 or channel > self.channel_amount:
            logger.error(f"[{self.id}] wrong channel: {channel}")
            return 3

        # data = wave + [0] * (32 - (len(wave) & 31)) #补齐32个采样点
        # data = [int(d + self.data_offset[channel - 1] + 32768) for d in data]
        # data = np.clip(data, 0, 65535).tolist()

        data = self.wave_calc_fast(channel, offset, wave)

        start_addr = ((channel - 1) << 19) + 2 * offset
        if self.batch_mode:
            self.waves[channel - 1] = wave.tobytes()
            return 0
            # ret = self.fast_write_memory(start_addr, data)
        else:
            ret = self.write_memory(start_addr, data)
        # length = len(data) * 2
        # ret = self.write_memory(0x00000004, start_addr, length, data)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s write wave failed, return is: %d!", self.id, ret)
        return ret
    #不要改动
    #   写序列
    def write_seq(self, channel, offset=0, seq=None, fast = False):
        if channel < 1 or channel > self.channel_amount:
            logger.error('Wrong Channel')
            return 3
        if not (len(seq) & 31) == 0:
            data = seq + [0] * (32 - (len(seq) & 31))
        else:
            data = seq
        start_addr = ((channel * 2 - 1) << 18) + offset * 8  # 序列的内存起始地址，单位是字节
        # start_addr = (channel * 2 - 1) * (1 << 18) + offset * 8  # 序列的内存起始地址，单位是字节
        if self.batch_mode:
            self.seqs[channel - 1] = data
            return 0
            # ret = self.fast_write_memory(start_addr, data)
        else:
            ret = self.write_memory(start_addr, data)
        # length_temp = len(data) * 2  # 字节个数
        # ret = self.write_memory(0x00000004, start_addr, length_temp, data)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s write seq failed!", self.id)
        return ret
    def write_seq_fast(self, channel, offset=0, seq=None):
        if channel < 1 or channel > self.channel_amount:
            logger.error('Wrong Channel')
            return 3
        if not (len(seq) & 31) == 0:
            data = seq + [0] * (32 - (len(seq) & 31))
        else:
            data = seq
        start_addr = ((channel * 2 - 1) << 18) + offset * 8  # 序列的内存起始地址，单位是字节
        # start_addr = (channel * 2 - 1) * (1 << 18) + offset * 8  # 序列的内存起始地址，单位是字节
        if self.batch_mode:
            self.seqs[channel - 1] = seq.tobytes()
            return 0
            # ret = self.fast_write_memory(start_addr, data)
        else:
            ret = self.write_memory(start_addr, data)
        # length_temp = len(data) * 2  # 字节个数
        # ret = self.write_memory(0x00000004, start_addr, length_temp, data)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s write seq failed!", self.id)
        return ret
    #   初始化设备
    #   1、硬件状态检测，读取状态寄存器，若状态异常，则进行硬件初始化（init_board），初始化后重新检测硬件状态；
    #   重复该步骤知道硬件状态正常或达到最大尝试次数，若最终状态为异常，则报错并推出初始化流程
    #   2、默认参数配置
    #   3、设置通道增益、通道默认电压值
    #   4、打开DA芯片

    def init_device(self):
        is_ready = self.is_mock
        try_count = 10
        while try_count > 0 and is_ready == 0:
            if self.read_device_status()==0:
                is_ready=1
            else:
                self.init_board()
                try_count = try_count - 1
                time.sleep(1)
        if is_ready == 0:
            logger.error("init device failed")
            return 3

        self.set_time_out(0, 2)
        self.set_time_out(1, 2)
        self.set_trig_interval_l1(self.trig_interval_l1_info)
        self.set_loop(1, 1, 1, 1)
        self.set_da_output_delay(self.output_delay_info)
        self.set_trig_delay(200e-9)
        self.set_trig_count_l2(1)
        self.set_trig_interval_l2(0.001)
        self.stop_output_wave(0)
        self.clear_trig_count()

        for k in range(0, self.channel_amount):
            self.set_gain(k + 1, self.channel_gain_info[k])  # channel start from 1
            self.set_default_volt(k + 1, self.channel_default_voltage_info[k])
        if self.batch_mode:
            self.commit_para()
            self.wait_response()
            self.set_monitor(1) ## 使能触发，并设置状态包发送的目的ip
        self.check_status()
        return 0

    def read_device_status(self):        
        ref = self.read_da_hardware_status()
        offset = [121, 202, 203, 204, 205, 321, 402, 403, 404, 405, 722]#, 732]
        mask = [0b11000000, 255, 255, 255, 255, 0b11000000, 255, 255, 255, 255, 0b00000000]
        expection = [0b11000000, 255, 255, 255, 255, 0b11000000,255,255,255,255,0b00000000]
        for (a, b, c) in zip(offset, mask, expection):
            if ref[a] & b != c:
                return 1
        return 0

    def init_board(self):
        ret = self.write_command(0x00001A05, 11, 1 << 16)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s init board failed!", self.id)
        return ret

    def sync_ctrl(self, id, val):
        self.set_para(0, 0x40, id | val)
        if id == 2:
            self.set_para(0, 0x40, val | 2)
            self.set_para(0, 0x40, (val+(4<<16))  | 3)
        if id == 4:
            self.set_para(0, 0x40, val | 4)
            self.set_para(0, 0x40, (val + (4 << 16)) | 5)
        if id == 9:
            if (val >> 12) > 65535:
                self.set_para(0, 0x40, (65535 << 16) | 1)
            elif (val >> 12) <= 0:
                self.set_para(0, 0x40, ((4 * 250) << 16) | 1)
            else:
                self.set_para(0, 0x40, (val << 4) | 1)
        # self.commit_para()

    def power_on_dac(self, chip, on_off):
        assert chip in [1,2]
        if self.batch_mode:
            self.set_para(chip, 0x011, on_off)
            return 0
        ret = self.write_command(0x00001E05, chip, on_off)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s power on failed!", self.id)
        return ret

    def start_stop(self, index):
        if self.batch_mode:
            self.set_para(0, 0x20, 0)
            self.set_para(0, 0x20, index)
            return 0
        ret = self.write_command(0x00000405, index, 0)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s start_stop failed!", self.id)
        return ret

    def set_loop(self, arg1, arg2, arg3, arg4):
        if self.batch_mode:
            self.set_para(0, 0x21, (arg1 << 16) | arg2)
            self.set_para(0, 0x23, (arg3 << 16) | arg4)
            return 0
        para1 = arg1 * 2 ** 16 + arg2
        para2 = arg3 * 2 ** 16 + arg4
        ret = self.write_command(0x00000905, para1, para2)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s set_loop failed!", self.id)
        return ret

    def set_dac_start(self, count):
        assert count < 65536
        count_trans = round(count) << 16
        
        if count_trans > 2**32-1:
            logger.error("set_dac_start count param error!")
            ret=1
            return ret
        if count != round(count):
            real=round(count)*4
            logger.warn("Da_output_delay should be a multiple of 4ns,otherwise we'll round it up.In this case,the real value of da_output_delay is {}ns".format(real))
        ret = self.write_command(0x00001805, 2, count_trans)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s set_dac_start failed!", self.id)
        return ret

    def set_trig_start(self, count):
        assert count < 65536
        count_trans = round(count) << 16
        if count_trans > 2**32-1:
            logger.error("set_trig_start count param out of range,trig_delay should be less than 262.13e-6!")
            ret=1
            return ret
        if abs(count - round(count))>0.1:
            real=round(count)*4
            logger.warn("Trig_delay should be a multiple of 4ns,otherwise we'll round it up.In this case,the real value of trig_delay is {}ns".format(real))
        ret = self.write_command(0x00001805, 4, count_trans)

        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s set_trig_start failed!", self.id)
        return ret

    def set_trig_stop(self, count):
        assert count < 65536
        count_trans = round(count) << 16
        if count_trans > 2**32-1:
            logger.error("set_trig_stop count param out of range,width+trig_delay should be less than 262.14e-6!")
            ret=1
            return ret
        if abs(count - round(count))>0.1:
            real=round(count)*4
            logger.warn("Width+trig_delay should be a multiple of 4ns,otherwise we'll round it up.In this case,the real value of width+trig_delay is {}ns".format(real))
        ret = self.write_command(0x00001805, 5, count_trans)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s set_trig_stop failed!", self.id)
        return ret


    def send_int_trig(self):
        '''触发使能, 这条指令应该直接执行'''
        # if self.batch_mode:
        #     self.sync_ctrl(8,1 << 16)
        #     return self.commit_para()
        ret = self.write_command(0x00001805, 8, 1 << 16)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s send_int_trig failed!", self.id)
        return ret

    def set_trig_interval_l1(self, trig_interval):
        if trig_interval == self.trig_interval_l1:
            # print('set_trig_interval_l1 is same.')
            return 0
        else:
            count = trig_interval / 4e-9
            count_trans = round(count) << 12
            if count_trans > 2**32-1:
                logger.error("Interval_l1 count param out of range,interval_l1 should be less than 4.19e-3!")
                ret=1
                return ret
            if abs(count - round(count))>0.1:
                real=round(count)*4
                logger.warn("Interval_l1 should be a multiple of 4ns,otherwise we'll round it up.In this case,the real value of interval_l1 is {}ns".format(real))
            if self.batch_mode:
                self.sync_ctrl(9, count_trans)
                self.trig_interval_l1=trig_interval
                return 0
            ret = self.write_command(0x00001805,  9, count_trans)

            if not ret == 0:
                self.disp_error(ret)
                logger.error("DAC %s set_trig_interval failed!", self.id)
            else:
                self.trig_interval_l1=trig_interval
            return ret

    def set_trig_interval_l2(self, trig_interval):
        if trig_interval == self.trig_interval_l2:
            # print('set_trig_interval_l2 is same.')
            return 0
        else:
            count = trig_interval/ 4e-9
            count_trans = round(count) << 12
            if count_trans > 2**32-1:
                logger.error("Interval_l2 count param out of range,interval_l2 should be less than 4.19e-3!")
                ret=1
                return ret
            if abs(count - round(count))>1e-9:
                real=round(count)*4
                logger.warn("Interval_l2 should be a multiple of 4ns,otherwise we'll round it up.In this case,the real value of interval_l2 is {}ns".format(real))
            if self.batch_mode:
                self.sync_ctrl(15, count_trans)
                self.trig_interval_l2=trig_interval
                return 0
            ret = self.write_command(0x00001805,  15, count_trans)
            if not ret == 0:
                self.disp_error(ret)
                logger.error("DAC %s set_trig_interval failed!", self.id)
            else:
                self.trig_interval_l2=trig_interval
            return ret


    def set_trig_count_l1(self, count):
        if self.batch_mode:
            self.sync_ctrl(10, count << 12)
            self.trig_count_l1 = count
            return 0
        if count == self.trig_count_l1:
            # print('self.trig_count_l1 is same')
            return 0
        else:
            ret = self.write_command(0x00001805,  10, count << 12)
            if not ret == 0:
                self.disp_error(ret)
                logger.error("DAC %s set_trig_count failed!", self.id)
            else:
                self.trig_count_l1 = count
            return ret

    def set_trig_count_l2(self, count):
        if count == self.trig_count_l2:
            # print('self.trig_count_l2 is same')
            return 0
        else:
            if self.batch_mode:
                self.sync_ctrl(16,count << 12)
                self.trig_count_l2 = count
                return 0
            ret = self.write_command(0x00001805,  16, count << 12)
            if not ret == 0:
                self.disp_error(ret)
                logger.error("DAC %s set_trig_count failed!", self.id)
            else:
                self.trig_count_l2 = count
            return ret

    def set_monitor(self, enable = 1):
        _ip_para = 0
        for idx, _d in enumerate(self.host_ip.split('.')):
            _ip_para = int(_d) << (24 - idx * 8)
        self.write_command(0x00001305, enable, _ip_para)
        return 0

    def clear_trig_count(self):
        if self.batch_mode:
            self.sync_ctrl(11,1 << 16)
            return 0
        ret = self.write_command(0x00001F05, 0, 0)
        if not ret == 0:
            self.disp_error(ret)
            logger.error("DAC %s set_trig_count failed!", self.id)
        return ret

    #   读取AD9136芯片寄存器
    def read_ad9136(self, chip, addr):
        # ret = 0
        if chip == 1:
            return self.Read_Reg(0x1c,addr)
            # self.write_command(0x00001c05, addr, 0)
        else:
            return self.Read_Reg(0x1d,addr)
            # self.write_command(0x00001d05, addr, 0)
        # value = self.get_return(1)
        # return value.resp_data

    #   设置DA板的通信超时时间，direction代表方向，0为发送，1为输出，单位为秒
    def set_time_out(self, direction, time):
        return 0
        # dll_func = self.dll.SetTimeOut
        # ret = dll_func(self.f_id, direction, time)
        # if not ret == 0:
        #     self.disp_error(ret)
        #     logger.error("DAC %s set_time_out failed!", self.id)
        # return ret

    def set_trig_delay(self, point, width=10*4e-9):
        count = int((self.da_trig_delay_offset + point) / 4e-9 + 1)
        assert count+10 < 65536
        if self.batch_mode:
            self.sync_ctrl(4,count << 16)
            self.sync_ctrl(5,(count+10) << 16)
            return 0
        if not point == self.trig_delay:
            ret1 = self.set_trig_start((self.da_trig_delay_offset + point) / 4e-9 + 1)
            self.trig_delay = point
            ret2 = self.set_trig_stop((self.da_trig_delay_offset + point) / 4e-9 + width/4e-9)
            self.trig_delay_width=width
            return ret1 | ret2
        elif not width == self.trig_delay_width:
            ret2 = self.set_trig_stop((self.da_trig_delay_offset + point) / 4e-9 + width/4e-9)
            self.trig_delay_width=width
            return ret2
        else:
            print('set_trig_delay is same')
            return 0

    def set_da_output_delay(self, delay):
        count = int((delay) / 4e-9 + 1)
        assert count+10 < 65536
        if self.batch_mode:
            self.sync_ctrl(2,count << 16)
            self.sync_ctrl(3,(count+10) << 16)
            return 0
        if not delay == self.output_delay:
            ret1 = self.set_dac_start(delay / 4e-9 + 1)
            # ret2 = self.set_dac_stop(sync_delay / 4e-9 + 10)
            self.output_delay=delay
            return ret1
        else:
            # print('set_da_output_delay is same.')
            return 0

    #   设置通道增益，对应bank值为7
    def set_gain(self, channel, gain):
        if gain < 0:
                gain += 1024
        if gain == self.channel_gain[channel-1]:
            # print('gain is same.')
            return 0
        else:
            # if gain < 0:
            #     gain += 1024
            channel_map = [2, 3, 0, 1]
            channel_ad = channel_map[channel - 1]
            if self.batch_mode:
                chip_sel = (channel_ad >> 1) + 1
                addr = 0x040 + ((channel_ad & 0x01) << 2)
                self.set_para(chip_sel, addr, (gain >> 8) & 0x03)
                self.set_para(chip_sel, addr + 1, gain & 0xFF)
                return 0
            ret = self.write_command(0x00000702, channel_ad, gain)
            if not ret == 0:
                self.disp_error(ret)
                logger.error("DAC %s set_gain failed!", self.id)
            self.channel_gain[channel-1]=gain
            return ret

    # #   设置通道偏置，对应bank值为7
    # def set_channel_offset(self, channel, offset):
    #     channel_map = [6, 7, 4, 5]
    #     channel_ad = channel_map[channel - 1]
    #     ret = self.write_command(0x00000702, channel_ad, int(offset))
    #     if not ret == 0:
    #         self.disp_error(ret)
    #         logger.error("DAC %s set_channel_offset failed!", self.id)
    #     self.channel_offset[channel-1]=offset
    #     return ret

    #   设置通道默认电压
    def set_default_volt(self, channel, volt):
        offset=self.data_offset[channel - 1]
        if volt != -1:
            channel = channel - 1
            volt = volt + self.channel_voltage_offset[channel]
            if volt > 65535:
                volt = 65534
            if volt < 0:
                volt = 0
            volt = 65535 - volt
        else:# hold模式 1 to 3 2 to 4 3to 5
            channel = channel + 3
            volt = 32768

        if self.batch_mode:
            _code = volt+offset
            _code1 = (_code & 0xFF << 24) | (_code & 0xFF00 << 8)
            self.set_para(0, 0x41, (_code1 | channel))
            self.channel_default_voltage[channel-1]=volt
            return 0

        if not volt==self.channel_default_voltage[channel-1]:
            ret = self.write_command(0x00001B05, channel, int(volt+offset))
            self.channel_default_voltage[channel-1]=volt
            if not ret == 0:
                self.disp_error(ret)
                logger.error("DAC %s set_default_volt failed!", self.id)

        else:
            # print('default_vol is same')
            ret=0

        return ret

    #   开始波形输出，打开某一个通道；channel为0时，打开所有通道
    def start_output_wave(self, channel):
        ret = 0
        if channel > 0 and channel < self.channel_amount + 1:
            index = 1 << (channel - 1)
            ret = self.start_stop(index)
            if not ret == 0:
                self.disp_error(ret)
                logger.error("DAC %s start_output_wave failed!", self.id)
        elif channel == 0:
            ret=0
            for i in range(1,self.channel_amount+1):
                index = 1 << (i - 1)
                ret0 = self.start_stop(index)
                if not ret0 == 0:
                    self.disp_error(ret)
                    logger.error("DAC %s start_output_wave failed!", self.id)
                    ret=ret0
        return ret

    #   停止波形输出，关闭某一个通道
    def stop_output_wave(self, channel):
        if channel > 0:
            index = 1 << (channel - 1 + self.channel_amount)
            ret = self.start_stop(index)
            if not ret == 0:
                self.disp_error(ret)
                logger.error("DAC {} channel {} stop_output_wave failed!".format(self.id, channel))
                # logger.error("DAC %s stop_output_wave failed!", self.id)
        elif channel==0:
            ret=0
            for i in range(1,self.channel_amount+1):#遍历所有通道
                index = 1 << (i - 1 + self.channel_amount)
                ret0= self.start_stop(index)
                if not ret0 == 0:
                    self.disp_error(ret)
                    logger.error("DAC {} channel {} stop_output_wave failed!".format(self.id,i))
                    # logger.error("DAC %s stop_output_wave failed!", self.id)
                    ret=ret0
        return ret
        # self.start_stop(240)

    #   获取当前调用位置函数调用信息
    def get_func_type(self, offset):
        return 0
        # func_types = ["Write instruction type.", "Write memory type.", "Read memory type."]
        # dll_func = self.dll.GetFunctionType
        # func_type = ctypes.c_int()
        # ins = ctypes.c_int()
        # para1 = ctypes.c_int()
        # para2 = ctypes.c_int()
        # ret = dll_func(self.f_id, offset, ctypes.byref(func_type), ctypes.byref(ins), ctypes.byref(para1),
        #                ctypes.byref(para2))
        # self.disp_error(ret)
        # func_type = func_type.value
        # ins = ins.value
        # para1 = para1.value
        # para2 = para2.value
        # func_type_obj = FuncType(func_type, ins, para1, para2, func_types[func_type - 1])
        # return func_type_obj

    #   获取返回值
    def get_return(self, offset):
        return 0
        # func_type = self.get_func_type(1)
        # if func_type.func_type == 1:
        #     length = 0
        # else:
        #     length = func_type.para2 / 2
        # PData = ctypes.c_ushort * int(length)
        # resp_stat = ctypes.c_int()
        # resp_data = ctypes.c_int()
        # data = PData()
        # dll_func = self.dll.GetReturn
        # ret = dll_func(self.f_id, offset, ctypes.byref(resp_stat), ctypes.byref(resp_data), data)
        # self.disp_error(ret)
        # resp_stat = resp_stat.value
        # resp_data = resp_data.value
        # result = RetResult(resp_stat, resp_data, bytes(data))
        # return result

    #   根据错误码获取错误信息
    def disp_error(self, error_code):
        # if not error_code == 0:
        #     dll_func = self.dll.GetErrorMsg
        #     error_msg = ctypes.create_string_buffer(1024)
        #     dll_func(error_code, error_msg)
        #     logger.error(error_msg.value)
        return 0

    #   读取芯片温度，预留，有多个芯片，但参数列表仅有target标识
    def get_da_temperature(self, chip):
        tt1 = self.read_ad9136(chip, 0x132)
        tt2 = self.read_ad9136(chip, 0x133)
        tt1 = float(divmod(tt1, 256)[1])
        tt2 = float(divmod(tt2, 256)[1])
        result = 30 + 7.3 * (tt2 * 256 + tt1 - 39200) / 1000.0
        return result

    def check_status(self):
        # dll_func = self.dll.CheckSuccessed
        # is_success = ctypes.c_int()
        # position = ctypes.c_int()
        # ret = dll_func(self.f_id, ctypes.byref(is_success), ctypes.byref(position))
        # if not ret == RetResult.OK:
        #     self.disp_error(ret)
        #     logger.error("DAC %s check_status failed!", self.id)
        # return (ret, is_success.value, position.value) if not self.is_mock else (0, 1, 0)
        return (0, 1, 0)

    #主动读取DA板硬件信息，大小为1k
    def read_da_hardware_status(self):
        # self.read_memory(0x00000003, 0x80000000, 1024)
        # result = self.get_return(1)
        # return result
        return self.read_memory(0x80000000, 1024)

    # 设置数据偏置
    def set_data_offset(self, channel, offset):
        self.data_offset[channel - 1] = offset
        return 0

    # def DA_reset(self):
    #     """Run command."""
    #     print('da reset please wait 20 seconds')
    #     cmd = self.board_def.CMD_CTRL_CMD
    #     ctrl = self.board_def.CTRL_REINIT
    #     data0 = 1
    #     data1 = 0
    #     packedCtrl = struct.pack("l", ctrl)
    #     unpackedCtrl = struct.unpack('4b', packedCtrl)
    #     packet = struct.pack("4bLL", cmd, unpackedCtrl[0], unpackedCtrl[1], unpackedCtrl[2], data0, data1)
    # #    print ('this is my cmd packet: {}'.format(repr(packet)))
    #     self.send_data(packet)
    #     time.sleep(5)
    #     print('da reset done')
    #     return 0
    def DA_reprog(self):
        """Run command."""
        print('da reprog please wait 10 seconds')
        packet = struct.pack("LLL", 0x00000105, 2, 1)
        self.send_data(packet)
        time.sleep(10)
        self.connect()
        print('da reprog done')
        return 0


    def init_tcp(self):
        init_cmd = struct.pack('I', 0xDEADBEEF)
        self.sockfd.send(init_cmd*3)
