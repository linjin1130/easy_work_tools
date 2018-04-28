
import os
import struct
dir = 'E:\\工程相关\\DPS实验\\DPS实验数据\\'
recv_dps_file = dir+'20150325000845-R-APD2-091.dat'
rndfilepath = dir+"_接收端随机数.dat"
mixrndfilepath = dir+"_混合随机数.dat"
psfilepath = dir+"_稳相数据.dat"
pmrfilepath = dir+"_稳相结果.dat"

fd_rndfilepath = open(rndfilepath,'wb')
fd_mixrndfilepath = open(mixrndfilepath,'wb')
fd_psfilepath = open(psfilepath,'wb')
fd_pmrfilepath = open(pmrfilepath,'wb')

ps_md_file = dir+"稳相算法中间数据.dat"
fd_ps_md_file = open(ps_md_file, 'wb')
# with open(recv_dps_file, 'rb') as rd_fd:
#     for line in rd_fd.read(2048):
#         print(len(line))
def data_process(data):
    # fmt = '8s2032s8s'
    # data2 = struct.unpack(fmt, data)[1]
    # data1 = data[8:-8]
    # print(data1)
    # print(data2)

    for i in range(1,254):
        item = data[i*8:i*8+8]
        if item[1] == 0xAA:
            print(1)
        elif item[1] == 0xBB:
            if item[3] == 0xA0:
                poc_num = ((item[4] & 0x0F) << 4) | (item[7] & 0xF0) >> 4
                fd_ps_md_file.write()
        else:
            print(item)
            print('error')

fd = open(recv_dps_file, 'rb')

data = fd.read(2048)
while(len(data) ==2048):
    data_process(data)
    data = fd.read(2048)