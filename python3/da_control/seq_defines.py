# -*- coding: utf-8 -*-
import struct
from math import floor

# DA板序列控制定义，控制波形输出的核心
# seq[4 * k] = 0    # start_addr
# seq[4 * k + 1] = 5 # length
# seq[4 * k + 2] = 2000 # repeat_trig or count
# seq[4 * k + 3] = 16384  # 触发
# def generate_trig_seq(length, delay, channel_output_delay):
#     # length = round(length / 8) # why ?
#     length = (length >> 3)
#     ch_delay = round(channel_output_delay / 4e-9)
#     return [0, length, ch_delay, 16384|0x8000]+[0]*12

def generate_trig_seq(loop_cnt, trig_interval, length, channel_output_delay):
    print("generate trig seq ", trig_interval, length)
    seq_trig_delay_cnt = 45
    trig_flag = 1 << 10
    idle_wave_len = 5
    ## 输出波形的最小长度为20ns 即 5个时钟计数
    assert idle_wave_len > 4
    assert length > 4*8
    wave_len = (length + 7) >> 3
    # 1 触发指令
    func = 0x8 << 11 # trig seq
    ctrl = func
    ch_delay = round(channel_output_delay / 4e-9)
    seq_T =  [0,idle_wave_len,ch_delay,ctrl]

    # 2 1级循环开始
    func = 0x1 << 11
    loop_level = 0
    ctrl = func | (loop_level << 8)
    seq_L1 =  [0,idle_wave_len,loop_cnt,ctrl]

    # 3 等待计时
    func = 0x4 << 11
    wait_cnt = round(trig_interval / 4e-9) - 10 -(wave_len)
    # 10 是两条循环指令的执行开销, (length >> 3)是波形本身长度
    ctrl = func | trig_flag | seq_trig_delay_cnt
    seq_C = [idle_wave_len, wave_len, wait_cnt, ctrl]

    # 4 1级循环结束
    func = 0x2 << 11
    loop_level = 0
    jump_addr = 1
    ctrl = func | (loop_level << 8)
    seq_J1 =  [0,idle_wave_len,jump_addr,ctrl]

    # 5 停止输出
    func = 0x4 << 11
    stop = 1 << 15
    ctrl = func | stop
    seq_S =  [0,idle_wave_len,4,ctrl]

    seq = seq_T + seq_L1 + seq_C + seq_J1 + seq_S
    seq = seq + [32768] * (32 - (len(seq) & 31))
    # 为了64字节对齐
    # print(seq)
    # fmt = f'{len(seq)}H'
    # seq=struct.pack(fmt,*seq)
    # print(seq)
    return seq

def generate_continuous_seq(count):
    count_temp = (count >> 3)
    seq = [0, count_temp, 0, 0] * 4096
    # fmt = f'{len(seq)}H'
    # seq=struct.pack(fmt,*seq)
    return seq



# def bin_to_dec(fun_ctrl):
#     num = 0
#     while fun_ctrl:
#         num = num*2+eval(fun_ctrl[0])
#         fun_ctrl = fun_ctrl[1:]
#     return num


# def generate_seq(mode, length, stop_flag=0, trig_flag=0
#                  , trig_delay=0, loop_level=0, delay=0, count=0, Ax_N=0, Ax_0=0, Ax=0, Ax_1=0, Ax_2=0):
#
#     # [Ax[15..0], L[15..0], C[15..0], F[7..0]*256 + T[7..0]]
#     # mode 0-触发模式 1-连续输出模式 2-延时输出模式 3-条件输出模式 4-循环开始序列标识 5-循环结束序列标识
#     if isinstance(mode, dict):
#         keys = mode.keys()
#         if 'stop_flag' in keys:
#             stop_flag = mode['stop_flag']
#         if 'trig_flag' in keys:
#             trig_flag = mode['trig_flag']
#         if 'trig_delay' in keys:
#             trig_delay = mode['trig_delay']
#         if 'loop_level' in keys:
#             loop_level = mode['loop_level']
#         if 'delay' in keys:
#             delay = mode['delay']
#         if 'count' in keys:
#             count = mode['count']
#         # if 'Ax_N' in keys:
#         #     Ax_N = mode['Ax_N']
#         # if 'Ax_0' in keys:
#         #     Ax_0 = mode['Ax_0']
#         # if 'Ax' in keys:
#         #     Ax = mode['Ax']
#         # if 'Ax_1' in keys:
#         #     Ax_1 = mode['Ax_1']
#         # if 'Ax_2' in keys:
#         #     Ax_2 = mode['Ax_2']
#         length = mode['length']
#         mode = mode['mode']
#     length = (length >> 3)  # 8位为一个地址，计算需要存几个地址
#     if mode == 0:  # t trigger
#         fun_ctrl = str(stop_flag) + "1000" + str(trig_flag) + "00"
#         dec_fun_ctrl = bin_to_dec(fun_ctrl) * 256 + trig_delay
#         ch_delay = round(delay / 4e-9)
#         if (delay-ch_delay) > 0.1:
#             logger.warn(
#                 "The count of the trigger instruction waiting time, each count representing 4ns."
#                 "In this case,the real value of delay is {}ns".format(ch_delay*4))
#         return [Ax, length, ch_delay, dec_fun_ctrl]
#     if mode == 1:  # s 连续输出模式 continuous_output
#         fun_ctrl = str(stop_flag) + "0000" + str(trig_flag) + "00"
#         dec_fun_ctrl = bin_to_dec(fun_ctrl) * 256 + trig_delay
#         return [Ax, length, 0, dec_fun_ctrl]
#
#     if mode == 2:  # d 延时输出模式 d_output
#         fun_ctrl = str(stop_flag) + "0100" + str(trig_flag) + "00"
#         dec_fun_ctrl = bin_to_dec(fun_ctrl) * 256 + trig_delay
#         ch_delay = round(delay / 4e-9)  # 每一个计数代表4ns
#         if (delay-ch_delay) > 0.1:
#             logger.warn(
#                 "The count of the trigger instruction waiting time, each count representing 4ns."
#                 "In this case,the real value of delay is {}ns".format(ch_delay*4))
#         return [Ax, length, ch_delay, dec_fun_ctrl]
#     if mode == 3:  # c 条件输出模式 ?? 不确定 condition_output
#         fun_ctrl = str(stop_flag) + "1100" + str(trig_flag) + "00"
#         dec_fun_ctrl = bin_to_dec(fun_ctrl) * 256 + trig_delay
#         return [0, length, 0, dec_fun_ctrl]
#     if mode == 4:  # 循环开始序列标识 loop_start
#         loop_level_dict = {0: "00", 1: "01", 2: "10", 3: "11"}
#         fun_ctrl = str(stop_flag) + "0001" + str(trig_flag) + loop_level_dict[loop_level]
#         dec_fun_ctrl = bin_to_dec(fun_ctrl) * 256 + trig_delay
#         return [Ax, length, count, dec_fun_ctrl]
#     if mode == 5:  # 循环结束序列标识 loop_end
#         loop_level_dict = {0: "00", 1: "01", 2: "10", 3: "11"}
#         fun_ctrl = str(stop_flag) + "0002" + str(trig_flag) + loop_level_dict[loop_level]
#         dec_fun_ctrl = bin_to_dec(fun_ctrl) * 256 + trig_delay
#         return [Ax, length, count, dec_fun_ctrl]
