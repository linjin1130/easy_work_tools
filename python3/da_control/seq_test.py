import itertools
from DAboard import *
import filecmp
import logging
#setup
logging.basicConfig(level = logging.INFO,format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger()
logger.setLevel(logging.INFO)

import matplotlib.pyplot as plt
import random

## 参数集合
length_set = (4,16) ## 波形长度集合
addr_set = (0,16,48) ## 3种起始地址
delay_set = (0,10,20) #3种延时
trig_delay_set = (45,48) #3种延时
trig_type_set = (0,1) #两种触发类型
cmd_cnt_set = (1,2,3) ##指令重复条数组合
cmd_type_set = (0,4,12) ##,4种指令类型，LOOP和JUMP绑定使用，触发类型固定在第一条，便于测试

cycle_level_set = (0,1,2,3,4) ##4种循环级别+一种无循环
cycle_cnt_set = (1,3) ##2循环次数
cycle_pos_set = (0,2) ##循环指令在最终序列数据中的位置

first_seq = [0, 16, 0, 8<<11 | 1 << 10 | 45]
### 首先生成循环指令对集合
## 为了便于测试，第一条指令是触发指令
def get_length():
    return length_set[random.randint(0,len(length_set)-1)]

def get_addr(is_state=False):
    if is_state == 1:
        return 0x00010001
    else:
        return addr_set[random.randint(0,len(addr_set)-1)]

def get_count(is_state = False, is_count=False):
    if is_state == 1:
        return 0x00010001
    elif is_count==1:
        return delay_set[random.randint(0,len(delay_set)-1)]
    else:
        return 0

def get_seq_trig():
    return trig_type_set[random.randint(0,len(trig_type_set)-1)] << 10 | trig_delay_set[random.randint(0,len(trig_delay_set)-1)]


def gen_func_list():
    func_list = []
    for cmd_type in cmd_type_set:
        func_list.append([cmd_type << 11 , cmd_type == 4, cmd_type == 12])
    return func_list

def gen_cmd_no_loop(funcs):
    ## 生成无循环的序列指令
    seq_cmds = []
    logger.info('排列组合类型：{}取1'.format(len(funcs)))
    for idxs in itertools.permutations(range(len(funcs)), 1):
        seqs = []
        seqs += first_seq
        for idx in idxs:
            seqs += [get_addr(funcs[idx][2]), get_length(), get_count(funcs[idx][2], funcs[idx][1]), funcs[idx][0]|get_seq_trig()]
        seqs[-1] |= 0x8000
        seq_cmds.append([seqs])
    logger.info('排列组合类型：{}取{}'.format(len(funcs),len(funcs)))
    for idxs in itertools.permutations(range(len(funcs)), len(funcs)):
        seqs = []
        seqs += first_seq
        for idx in idxs:
            seqs += [get_addr(funcs[idx][2]), get_length(), get_count(funcs[idx][2], funcs[idx][1]), funcs[idx][0]|get_seq_trig()]
        seqs[-1] |= 0x8000
        seq_cmds.append([seqs])
    loop_seq = []
    logger.info('排列组合类型：{}取{},取出后*2'.format(len(funcs),len(funcs)))
    for idxs in itertools.permutations(range(len(funcs)), len(funcs)):
        seqs = []
        seqs += first_seq
        for idx in idxs:
            seqs += [get_addr(funcs[idx][2]), get_length(), get_count(funcs[idx][2], funcs[idx][1]), funcs[idx][0]|get_seq_trig()]
            seqs += [get_addr(funcs[idx][2]), get_length(), get_count(funcs[idx][2], funcs[idx][1]), funcs[idx][0]|get_seq_trig()]
        loop_seq = seqs.copy()
        seqs[-1] |= 0x8000
        seq_cmds.append([seqs])
    loop_seq = loop_seq+loop_seq[4:] ##不要第一个含触发的序列
    loop_seq[-1] |= 0x8000
    return seq_cmds, loop_seq
funcs = gen_func_list()
gen_cmd = gen_cmd_no_loop(funcs)

da_ctrl = waveform()
da_ctrl.generate_sin(repeat=100,cycle_count=5)
# da_ctrl.generate_seq(length=len(da_ctrl.wave)>>4)
# da_ctrl.gen_comp_wave()
# count_seq = [0, 64, 2, 4<<11]*2
tmp_wave = da_ctrl.wave[0:128]
da_ctrl.generate_sin(repeat=3,cycle_count=256)
tmp_wave += da_ctrl.wave[0:256]
# da_ctrl.generate_cos(repeat=3,cycle_count=256)
da_ctrl.generate_squr(repeat=4, hightime=320,lowtime1=160,lowtime2=160)
tmp_wave += da_ctrl.wave[0:640]
da_ctrl.wave = tmp_wave

for item in gen_cmd:
    da_ctrl.seq = item
    # sample_count,wave,trig_time = da_ctrl.wave_preview('无嵌套')


orig = ['()','[]','{}','<>']
rslt = ['','','','']
rslt = ['()','[]','{}','<>']
brack_dic = {'(':[0,1], '[':[1,1], '{':[2,1], '<':[3,1], ')':[0,-1], ']':[1,-1], '}':[2,-1], '>':[3,-1]}

def drop(brack_in):
    ## 丢弃同一级括号嵌套的模式和括号数大于5对的模式
    cnt = [0]*4
    for i in brack_in:
        cnt[brack_dic[i][0]] += brack_dic[i][1]
        if cnt[brack_dic[i][0]] > 1:
            return True
        if len(brack_in) > 8:
            return True
    return False

def insert_in(orig_in, ins_in):
    ## 括号插入
    new_items = []
    for item in orig_in:
        new_items.append(ins_in+item)
        for idx in range(1,len(item)):
            new_items.append(item[0:idx]+ins_in+item[idx:])
        # new_items.append(item+ins_in)
    return new_items

for item in orig:
    temp = []
    temp = insert_in(rslt, item)
    new_rs = []
    for item in temp:
        if not drop(item):
            new_rs.append(item)
    rslt += new_rs

for item in rslt:
    if not drop(item):
        new_rs.append(item)
    else:
        print('丢弃：{}'.format(item))

rslt = set(new_rs)

print(len(rslt))
logger.info('循环模式个数：{}'.format(len(rslt)))

def get_loop_mode():
    seq_flag_list = ['S','S','C','C','D','D','S','D','C','S','D','C']
    seq_flag_list = 'SSDDCCSDCSDC'
    seq_flag_list = '0123456789'
    list = [i for i in range(len(seq_flag_list))]

    seq_mod_set = []

    for item in set(new_rs):
        logger.debug('get_loop_mode中的括号模式：{}'.format(item))
        ## 生成要插入的位置
        ## 生成插入段数
        seg_cnt = random.randint(1,len(item)+1)
        ins_pos_list = random.sample([i for i in range(len(item)+1)],seg_cnt)
        ins_pos_list.sort()
        logger.debug('括号中的插入位置：{}'.format(ins_pos_list))
        ## seq序列分段位置
        slice = random.sample(list,seg_cnt-1)
        slice.sort()
        logger.debug('get_loop_mode中的分段：{}'.format(slice))
        ## 对seq分段
        pre_pos = 0
        seq_segs = []
        if seg_cnt == 1: #只分一段
            seq_segs.append(seq_flag_list)
        else:
            for pos in slice:
                seq_segs.append(seq_flag_list[pre_pos:pos])
                pre_pos = pos
        seq_segs.append(seq_flag_list[pre_pos:])
        ## seq分段插入括号中要插入的位置
        out = ''
        pre_pos = 0
        for idx, pos in enumerate(ins_pos_list):
            out += item[pre_pos:pos]+seq_segs[idx]
            pre_pos = pos
        out += item[pre_pos:]
        logger.debug('get_loop_mode中的模式：{}'.format(out))
        # yield out
        seq_mod_set.append(out)
    return seq_mod_set
addr = 0
length = 4
ctrl = 0x1 << 11
loop_cnt = 2
loop_level = 0
ctrl = ctrl | (loop_level << 8)
seq_L1 =  [addr,4,loop_cnt,ctrl]
# seq_L1


# ### 一级触发输出停止单元

# In[4]:


ctrl = 0x2 << 11
jump_addr = 1
loop_level = 0
ctrl = ctrl | (loop_level << 8)
seq_J1 =  [addr,4,jump_addr,ctrl]
# seq_J1


# ### 二级触发输出开始单元

# In[5]:


ctrl = 0x1 << 11
loop_cnt = 3
loop_level = 1
ctrl = ctrl | (loop_level << 8)
seq_L2 =  [addr,4,loop_cnt,ctrl]
# seq_L2


# ### 二级触发输出停止单元

# In[6]:


ctrl = 0x2 << 11
jump_addr = 2
loop_level = 1
ctrl = ctrl | (loop_level << 8)
seq_J2 =  [addr,4,jump_addr,ctrl]
# seq_J2


# ### 三级触发输出开始单元

# In[7]:


ctrl = 0x1 << 11
loop_cnt = 2
loop_level = 2
ctrl = ctrl | (loop_level << 8)
seq_L3 =  [addr,4,loop_cnt,ctrl]
# seq_L3


# ### 三级触发输出停止单元

# In[8]:


ctrl = 0x2 << 11
jump_addr = 3
loop_level = 2
ctrl = ctrl | (loop_level << 8)
seq_J3 =  [addr,4,jump_addr,ctrl]
# seq_J3


# ### 四级触发输出开始单元

# In[9]:


ctrl = 0x1 << 11
loop_cnt = 3
loop_level = 3
ctrl = ctrl | (loop_level << 8)
seq_L4 =  [addr,4,loop_cnt,ctrl]
# seq_L4


# ### 四级触发输出停止单元

# In[10]:


ctrl = 0x2 << 11
jump_addr = 8
loop_level = 3
ctrl = ctrl | (loop_level << 8)
seq_J4 =  [addr,4,jump_addr,ctrl]
# seq_J4

seq_head = da_ctrl.seq[0:4]
seq_tail = da_ctrl.seq[-4:]
seq_list = []
for idx in range(1,11):
    seq_list.append(da_ctrl.seq[idx<<2:(idx<<2)+4])
seq_list += [seq_L1,seq_L2,seq_L3,seq_L4,seq_J1,seq_J2,seq_J3,seq_J4]

seq_idx_dic = {}
for i in range(10):
    seq_idx_dic[str(i)] = i
for idx, key in enumerate(['(','[','{','<',')',']','}','>']):
    seq_idx_dic[key] = idx+10

def get_seq_from_seq_mod(mode):
    seq_out = []
    for flag in mode:
        seq_out += seq_list[seq_idx_dic[flag]]
    # print(seq_list[seq_idx_dic[flag]])
    return seq_out

mode_gen = get_loop_mode()
def get_loop_mode_str(seq):
    loop_mode = ''
    func_dic = {0:'S', 1:'L', 2:'J', 8:'T', 12:'C', 4:'D'}
    loop_dic = {0:'(', 1:'[', 2:'{', 3:'<'}
    jump_dic = {0:')', 1:']', 2:'}', 3:'>'}
    start_addr = [[],[],[],[]]
    for seq_idx in range(len(seq) >> 2):
        idx = seq_idx << 2
        func = (seq[idx+3] >> 11) & 0x000F
        # level = seq[idx] #老版本
        level = (seq[idx+3] >> 8) & 0x03
        count = seq[idx + 2]
        stop = (seq[idx + 3] >> 15) & 0x0001

        label = func_dic[func]
        if label=='L':
            label = str(count)+loop_dic[level]
            start_addr[level].append(seq_idx)
            print('{}层循环起始：地址：{}'.format(level,seq_idx))
        if label=='J':
            label = jump_dic[level]
            if len(start_addr[level])==0:
                print('错误：循环起始与结束不匹配:地址{}'.format(idx))
            seq[idx+2] = start_addr[level][-1]
            start_addr[level].pop()
            print('{}层循环结束：跳转：{}'.format(level, seq[idx+2]))
        loop_mode += label
        if stop==1:
            break
    return loop_mode
for mode in mode_gen:
    logger.info('序列模式：{}'.format(mode))
    da_ctrl.seq = seq_head+get_seq_from_seq_mod(mode)+seq_tail
    print(get_loop_mode_str(da_ctrl.seq))
    # sample_count,wave,trig_time = da_ctrl.wave_preview('无嵌套')
# def get_func():
#     ## 返回无触发类型功能标识
#     cmd_type = cmd_type_set[random.randint(len(cmd_type_set))]
#     trig_type = trig_type_set[random.randint(len(trig_type_set))]
#     trig_delay = 0
#     if trig_type == 1:
#         trig_delay = trig_delay_set[random.randint(len(trig_delay_set))]
#     return cmd_type << 11 | trig_type << 10 | trig_delay
#
# def gen_cmd():
# cmd_1 =
#
# 1.首先生成功能区
#
#
#
# da_ctrl = waveform()
# da_ctrl.generate_sin(repeat=128>>4, cycle_count=16, pad=1)
# wave_sin = da_ctrl.wave
# da_ctrl.generate_cos(repeat=128>>4, cycle_count=16, pad=1)
# wave_cos = da_ctrl.wave
# da_ctrl.generate_dc(dc_code=0, length=384, pad=1)
# wave_dc_lowx384 = da_ctrl.wave
# da_ctrl.generate_dc(dc_code=65535, length=512, pad=1)
# wave_dc_highx512 = da_ctrl.wave
# da_ctrl.generate_squr(repeat=128>>4, lowtime1=4, hightime=8, lowtime2=4, pad=1)
# wave_squr = da_ctrl.wave
# da_ctrl.generate_saw(repeat=128>>4, cycle_count=16, pad=1)
# wave_saw = da_ctrl.wave
# da_ctrl.generate_inv_saw(repeat=128>>4, cycle_count=16, pad=1)
# wave_saw_inv = da_ctrl.wave
#
# da_ctrl.generate_sin(repeat=0, cycle_count=100000, pad=1)
# wave_sin_50u = da_ctrl.wave
#
# waves = [wave_sin, wave_cos, wave_saw_inv, wave_saw,wave_squr]
# da_ctrl.wave = []
# for wave in waves:
#     # print('ooooo')
#     da_ctrl.wave.extend(wave)
#     da_ctrl.wave = da_ctrl.wave+wave_dc_lowx384
#     da_ctrl.wave = da_ctrl.wave+wave_dc_highx512
#     # print(da_ctrl.wave)
# wave_total = da_ctrl.wave
# #触发单元 正弦
# #触发类型，地址为0，长度为8ns,50us, 64ns ， 重复次数为0
# ctrl = 0x8 << 11
# start_addr = 0
# seq_T_low =  [start_addr,2,0,ctrl]
# seq_T_high =  [start_addr,100000>>3,0,ctrl]
# seq_T_nomal =  [start_addr,128>>3,0,ctrl]
#
# # 余弦
# #触发类型，地址为1024，长度为8ns,50us, 64ns ， 重复次数为0
# start_addr = 1024>>3
# seq_T1_low =  [start_addr,2,0,ctrl]
# seq_T1_high =  [start_addr,100000>>3,0,ctrl]
# seq_T1_nomal =  [start_addr,128>>3,0,ctrl]
#
# #触发类型，地址为0，长度为2， 重复次数分别为1 2 3
# start_addr = 0
# seq_T2_low =  [start_addr,2,1,ctrl]
# seq_T2_high =  [start_addr,100000>>3,2,ctrl]
# seq_T2_nomal =  [start_addr,128>>3,3,ctrl]
#
# #直接输出单元 余弦波
# #直接输出类型，地址为0，长度为8ns,50us, 64ns
# ctrl = 0x0 << 11
# start_addr = 2048>>3
# seq_S_low =  [start_addr,2,0,ctrl]
# seq_S_high =  [start_addr,100000>>3,0,ctrl]
# seq_S_nomal =  [start_addr,128>>3,0,ctrl]
#
# #计时输出单元  方波
# #计时输出类型，地址为0，长度为8ns，计时8ns;,50us,计时40us; 64ns, 计时40ns
# ctrl = 0x4 << 11
# start_addr = 2048>>3
# seq_D_low =  [start_addr,2,2,ctrl]
# seq_D_high =  [start_addr,100000>>3,10000,ctrl]
# seq_D_nomal =  [start_addr,128>>3,10,ctrl]
#
# #态判断输出单元
# ctrl = 0xC << 11
# start_addr1 = 0#1态
# start_addr2 = 2#2态
# start_addr3 = 4#NULL态
# start_addr4 = 6#0态
# seq_C_low =  [start_addr1<<8 | start_addr2,2,start_addr3<<8 | start_addr4,ctrl]
# seq_C_high =  [start_addr1<<8 | start_addr2,100000>>3,start_addr3<<8 | start_addr4,ctrl]
# seq_C_nomal =  [start_addr1<<8 | start_addr2,128>>3,start_addr3<<8 | start_addr4,ctrl]
# seq_C_low =  [start_addr2<<8 | start_addr3,2,start_addr4<<8 | start_addr1,ctrl]
# seq_C_low =  [start_addr3<<8 | start_addr4,2,start_addr1<<8 | start_addr2,ctrl]
# seq_C_low =  [start_addr4<<8 | start_addr1,2,start_addr2<<8 | start_addr3,ctrl]
# # seq_C_low =  [2,4,65535,ctrl]
#
# #1一级触发输出开始单元
# ctrl = 0x1 << 11
# loop_cnt = 1
# loop_level = 0
# seq_L1_low =  [loop_level,0,loop_cnt,ctrl]
# loop_level = 10
# seq_L1_nomal =  [loop_level,0,loop_cnt,ctrl]
#
# #1一级触发输出停止单元
# ctrl = 0x2 << 11
# jump_addr = 2
# loop_level = 0
# seq_J1_low =  [loop_level,0,jump_addr,ctrl]
#
# #1二级触发输出开始单元
# ctrl = 0x1 << 11
# loop_cnt = 1
# loop_level = 1
# seq_L2_low =  [loop_level,0,loop_cnt,ctrl]
# loop_level = 10
# seq_L2_nomal =  [loop_level,0,loop_cnt,ctrl]
#
# #1二级触发输出停止单元
# ctrl = 0x2 << 11
# jump_addr = 3
# loop_level = 1
# seq_J2_low =  [loop_level,0,jump_addr,ctrl]
#
# #1三级触发输出开始单元
# ctrl = 0x1 << 11
# loop_cnt = 1
# loop_level = 2
# seq_L3_low =  [loop_level,0,loop_cnt,ctrl]
# loop_level = 10
# seq_L3_nomal =  [loop_level,0,loop_cnt,ctrl]
#
# #1三级触发输出停止单元
# ctrl = 0x2 << 11
# jump_addr = 4
# loop_level = 2
# seq_J3_low =  [loop_level,0,jump_addr,ctrl]
#
# #1四级触发输出开始单元
# ctrl = 0x1 << 11
# loop_cnt = 1
# loop_level = 3
# seq_L4_low =  [loop_level,0,loop_cnt,ctrl]
# loop_level = 10
# seq_L4_nomal =  [loop_level,0,loop_cnt,ctrl]
#
# #1四级触发输出停止单元
# ctrl = 0x2 << 11
# jump_addr = 5
# loop_level = 3
# seq_J4_low =  [loop_level,0,jump_addr,ctrl]
#
# da = DABoard()
# new_ip = '10.0.5.2'
# board_status = da.connect(new_ip)
# # da.Run_Command(26,0,0)
# da.Init()
# da.InitBoard()
# da.SetGain(0, 511)
# da.SetGain(1, 511)
# da.SetGain(2, 511)
# da.SetGain(3, 511)
# da.SetTrigStart(2)
# da.SetDefaultVolt(1, 32768)
# da.SetDefaultVolt(2, 32768)
# da.SetDefaultVolt(3, 32768)
# da.SetDefaultVolt(4, 32768)
#
# seq_count = 1
# #########################################################
# #测试49
# #触发1次 循环3次 下限长度
# da_ctrl.seq.clear()
# da_ctrl.seq = seq_T_low +seq_D_low+seq_C_low
# # da_ctrl.seq = da_ctrl.seq+seq_T1_low
# da_ctrl.seq[-1] |= 32768
# da_ctrl.seq += [0,0,0,0]*10
# da_ctrl.wave = wave_total
# loopcnt = 3
# trig_seq_cnt = 1
# seq_count = 3
# trig_count = loopcnt * trig_seq_cnt
# da.SetLoop(loopcnt,loopcnt,loopcnt,loopcnt)
# #########################################################
#
# print(da_ctrl.seq)
# da.StartStop(240)
# da.WriteSeq(1,da_ctrl.seq)
# da.WriteWave(1,da_ctrl.wave)
# da.WriteSeq(2,da_ctrl.seq)
# da.WriteWave(2,da_ctrl.wave)
# da.WriteSeq(3,da_ctrl.seq)
# da.WriteWave(3,da_ctrl.wave)
# da.WriteSeq(4,da_ctrl.seq)
# da.WriteWave(4,da_ctrl.wave)
# trig_interval = max(10,da_ctrl.seq[1])
# if trig_interval < 58:
#     da.SetTrigStart(trig_interval-1)
#     print('触发间隔过小',trig_interval)
# da.SetTrigInterval((trig_interval + 4)* seq_count)
# da.SetTrigIntervalL2((trig_interval + 4)* seq_count)
# da.SetTrigCount(trig_count)
# da.SetTrigCountL2(1)
# da.StartStop(15)
# da.SendIntTrig()
#
# da.disconnect()
# if board_status < 0:
#     print('Failed to find board')