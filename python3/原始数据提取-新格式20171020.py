# -*- coding: utf-8 -*-
import time
def tic():
    globals()['tt'] = time.clock()
def toc():
    print('\nElapsed time: %.8f seconds\n' % (time.clock()-globals()['tt']))


import sys, os
import struct

filename = 'T2_QKDS_LZTX_SCI_20171216021029_20171216021629_0B'

folder = filename[filename.find('LZTX'):filename.find('LZTX')+23]
inpath = r'E:/WORK/9XX/9XX数据/raw_data/LZTX/' #原始数据的目录

opath = os.path.join(inpath,folder)
if(not os.path.exists(opath)):
    os.makedirs(opath)

station_seq = ['XL', 'NS', 'NS', 'NS']
mode_seq    = ['FF', 'FF', 'FF', 'JG']
#根据前一天的计划填写，只填写分发模式相关的

#如前一天计划为 兴隆（激光），兴隆（分发），兴隆（激光），南山（分发）

logname = os.path.join(opath, filename+'.log')
ipathname = os.path.join(inpath, filename+'.dat')
opathname = os.path.join(opath, filename)

#data_type = [b'\x0F\xB7', b'\x0C\xFF', b'\x0C\x6D',b'\x0A\x12']
data_type = ['0fb7', '0cff', '0c6d','0a12']
sub_type = ['0ff9',]
data_len = [[4086, 4080], [4084,4086,4084,4086,4086,4086,4084,4086,4086],[4012],[4086]]

filenames = {}
has_procceed = 0
for i in range(len(data_type)):
    ##print(i,data_type[i])
    for sub in sub_type:
        for num in range(5):
            tmpfile = opathname+'-'+data_type[i]+'-'+sub+'-'+str(num)+'.dat'
            key = data_type[i]+sub+str(num)
            filehd = open(tmpfile, 'wb')
            filenames[key] = filehd#生成键-值对
tic()
count_pre = 0
file_num= 0
PRE_VALUE = []
PRE_WRCNT = 0

log_file = open(logname, 'w')
log_file.write('原始数据处理信息：\n')
first = 1
if ipathname.endswith(".dat") and has_procceed == 0:
    input_file = open(ipathname, 'rb')
    line_num = 0;
    while 1:
        #format = '>2sH2s1sH1s4086s4s'  ##设置头部输入输出格式
        format = '>2sH2s4s4086s4s'
        data = input_file.read(4100)  ##读取前8个字节
        if (len(data) < 4100):
            #print(len(data))
            break
        line_num += 1
        values = struct.unpack(format, data)


        #if(((values[1]+0x3FFF)-counvt_pre)&0x3FFF > 2):
        err_data = 0
        if(values[1]&0x3FFF != (count_pre+1)&0x3FFF):
            if first == 0:
                log_file.write(str(values[1])+'\t编号不连续:前一个计数-'+str(count_pre&0xFFF)+'后一个计数-'+str(values[1]&0xFFF)+'\n')

        tmp_type = int(values[2].hex(), 16)
        if(tmp_type == 0x0FF9):
            if(values[4][-6:] != b'ZZZZZZ'):
                err_data = 1
                print(values[1],values[4][-6:])
                log_file.write(str(values[1]) + '\t数据内容异常' + '\t计数-' + str(
                    values[1] & 0xFFF) + '\n')
        else:
            print(tmp_type)

        tmpkey = (values[0].hex()) + values[2].hex() + str(file_num)
        count_pre = values[1]
        if err_data == 0:
            try:
                ff = filenames[tmpkey]
                if (line_num == 8225):
                    file_num += 1
                    line_num = 0
                    ff.write(values[4][:4080-3568])
                else:
                    ff.write(values[4][:4080])
            except:
                log_file.write('数据头部异常:类型-'+values[0]+'子类型-'+values[2])
                print(u'数据头部异常')

        first = 0
    input_file.close()
    print("finish")

#print(type(filenames))
toc()
tdc_file = []
for key in filenames.keys():
    #print(filenames[key])
    ffn = opathname+'-'+key[:4]+'-'+key[4:-1]+'-'+key[-1]+'.dat'
    ##print(os.path.getsize(ffn))
    filenames[key].close()
    #print(key,ffn.find('0fb707'))
    if(os.path.getsize(ffn) == 0):
        os.remove(ffn)
    else:
        tdc_file.append(key)
        print(key)
log_file.write('TDC数据处理信息：\n')
for nn in  tdc_file:

    syn_time_arr = []
    syn_corse = []
    path_head = opathname+'-'+nn[:4]+'-'+nn[4:-1]+'-'+nn[-1]
    path_tail = ['.dat', 'syn_time.csv', 'time.png', 'corse.png', 'processed.dat']
    chennal = ['c', 'd','f']
    input_file = open(path_head+path_tail[0], 'rb')
    #outputfile = open(path_head+path_tail[-1], 'wb')
    log_file.write(u'文件名：'+path_head+path_tail[0]+'\n')
    log_file.write('对应地面站：'+station_seq[tdc_file.index(nn)] + '\n')
    format = '>3s3sBB'  ##设置时间数据格式
    #ouput_file = open(path_head+path_tail[1], 'w')
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

log_file.close()
toc()

# import zipfile


# def zip_dir(dir_name, zipfile_name):
#     file_list = []
#     if (os.path.isfile(dir_name)):
#         file_list.append(dir_name)
#     else:
#         for root, dirs, files in os.walk(dir_name):
#             for name in files:
#                 file_list.append(os.path.join(root, name))
#     zf = zipfile.ZipFile(zipfile_name, 'w', zipfile.zlib.DEFLATED)
#     for tar in file_list:
#         arcname = tar[len(dir_name):]
#         zf.write(tar, arcname)
#     zf.close()
#
#
# print("zip directory:", opath)
# zipfile_name = folder + '.zip'
# zip_dir(opath, zipfile_name)
#
# print("压缩完成")

print("处理完成")


