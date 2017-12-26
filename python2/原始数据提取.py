# -*- coding: utf-8 -*-
##struct Header
##{
##    char[4] tag1;
##    char[2] segseq;
##    char[2] segsize;
##}
##struct data
##{
##    char[2] tag_data;
##    char[1] dataseq;
##    char[0] tag;
##    char[60] real_data;
##}
import time
def tic():
    globals()['tt'] = time.clock()
def toc():
    print('\nElapsed time: %.8f seconds\n' % (time.clock()-globals()['tt']))

def ByteToHex( bins ):
    """
    Convert a byte string to it's hex string representation e.g. for output.
    """
    return ''.join( [ "%02X" % x for x in bins ] ).strip()


import sys, os
import struct
inpath = r'E:/WORK/9XX/9XX数据/raw_data/LZTX'
filename = 'T2_QKDS_LZTX_SCI_20170210220908_20170211012244_0B'
station_seq = ['XL', 'XL', 'NS', 'NS']
logname = os.path.join(inpath, filename+'.log')
ipathname = os.path.join(inpath, filename+'.dat')
opathname = os.path.join(inpath, filename)

#data_type = [b'\x0F\xB7', b'\x0C\xFF', b'\x0C\x6D',b'\x0A\x12']
data_type = ['0fb7', '0cff', '0c6d','0a12']
sub_type = [['00','07'], ['00','03','0c','30','c0','c3','cc','f0','f3','fc'],['00'],['00']]
data_len = [[4086, 4080], [4084,4086,4084,4086,4086,4086,4084,4086,4086],[4012],[4086]]

filenames = {}
for i in range(len(data_type)):
    ##print(i,data_type[i])
    for sub in sub_type[i]:
        for num in range(5):
            tmpfile = opathname+'-'+data_type[i]+'-'+sub+'-'+str(num)+'.dat'
            key = data_type[i]+sub+str(num)
            #print(os.path.getsize(tmpfile))
            filehd = open(tmpfile, 'wb')
            filenames[key] = filehd#生成键-值对
            #print(key, filenames[key])

        #print(ipathname+str(data_type[i].hex())+sub)
        #output_file = open(ipathname+str(data_type[i])+sub, 'wb')
tic()
count_pre = 0
file_num= 0
PRE_VALUE = []
PRE_WRCNT = 0
if ipathname.endswith(".dat"):
    input_file = open(ipathname, 'rb')
    log_file = open(logname, 'w')
    log_file.write('原始数据处理信息：\n')
    while 1:
        format = '>2sH2s1sH1s4086s4s'  ##设置头部输入输出格式
        data = input_file.read(4100)  ##读取前8个字节

        if (len(data) < 4100):
            #print(len(data))
            break

        values = struct.unpack(format, data)
        #if(((values[1]+0x3FFF)-counvt_pre)&0x3FFF > 2):
        err_data = 0
        if(values[1]&0x3FFF!=(count_pre+1)&0x3FFF):
            log_file.write(str(values[1])+'\t编号不连续:前一个计数-'+str(count_pre&0xFFF)+'后一个计数-'+str(values[1]&0xFFF)+'\n')

        print('HHH',ByteToHex(values[3]))
        tmp_type =  int(ByteToHex(values[3]))
        if(tmp_type == 7):
            if(values[6][-6:] != b'ZZZZZZ'):
                err_data = 1
                print(values[1],values[6][-6:])
            #else:
                #print(values[1],values[6][-6:])
        else:
            print(tmp_type)

        #else:
         #   log_file.write(str(values[1] & 0x3FFF)+'\n')
        tmpkey = (ByteToHex(values[0])+ByteToHex(values[3])+str(file_num))
        count_pre = values[1]
        if err_data == 1:
            try:
                ff = filenames[tmpkey]
                ff.write(values[6][:values[4]])
            except:
                log_file.write('数据头部异常:类型-'+str(values[0])+'子类型-'+str(values[3]))
                print('数据头部异常')
            if (values[4] < 4000):
                file_num += 1
    input_file.close()
    print("finish")

#print(type(filenames))
toc()
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig
tdc_file = []
for key in filenames.keys():
    #print(filenames[key])
    ffn = opathname+'-'+key[:4]+'-'+key[4:6]+'-'+key[6:]+'.dat'
    ##print(os.path.getsize(ffn))
    filenames[key].close()
    #print(key,ffn.find('0fb707'))
    if(os.path.getsize(ffn) == 0):
        os.remove(ffn)
    elif( key.find('0fb707') >= 0):
        tdc_file.append(key)
        print(key)
log_file.write('TDC数据处理信息：\n')
for nn in  tdc_file:

    syn_time_arr = []
    syn_corse = []
    path_head = opathname+'-'+'0FB7-07-'+nn[6:]
    path_tail = ['.dat', 'syn_time.csv', 'time.png', 'corse.png', 'processed.dat']
    chennal = ['c', 'd','f']
    input_file = open(path_head+path_tail[0], 'rb')
    #outputfile = open(path_head+path_tail[-1], 'wb')
    log_file.write(u'文件名：'+path_head+path_tail[0]+'\n')
    log_file.write('对应地面站：'+station_seq[tdc_file.index(nn)] + '\n')
    format = '>3s3sBB'  ##设置时间数据格式
    ouput_file = open(path_head+path_tail[1], 'w')
    imgfile1 = path_head+path_tail[2]
    imgfile2 = path_head + path_tail[3]
    syn_time = 0
    apd_time = 0
    pre_corse = 0
    corse_over_cnt = 0
    pre_tdc_num = 0
    toc()
    while(1):
        data = input_file.read(8)  ##读取前16个字节
        if(len(data)<8) or (data[7]==0x5A):
            break
        values = struct.unpack(format, data)

        if((values[3] & 0xF0) != 0xF0):
            continue

        count = int(values[0].hex(), 16)
        course = int(values[1].hex(), 16)
        if course < pre_corse :
            corse_over_cnt += 1
        #syn_time = (course + (corse_over_cnt << 24)) + values[2]/256.0 #单位是ps
        #ouput_file.write(str(syn_time)+','+str((course+0xFFFFFF-pre_corse)%0xFFFFFF)+'\n')
        if(int(values[0].hex(), 16) - pre_tdc_num) > 5:
            log_file.write(u'TDC计数编号缺失区间：' + str(pre_tdc_num) + '-' + str(int(values[0].hex(),16)) + '\n')
        pre_tdc_num = int(values[0].hex(), 16)
        #syn_time_arr.append(syn_time)
        delta_corse = (course+0xFFFFFF-pre_corse)%0xFFFFFF
        syn_corse.append(delta_corse)
        pre_corse = course
    #plt.plot(syn_time_arr)
    #savefig(imgfile1)
    #plt.clf()
    #plt.close()
    plt.plot(syn_corse)
    savefig(imgfile2)
    plt.clf()
    plt.close()

log_file.close()
toc()