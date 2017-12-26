# -*- coding:cp936 -*- 
import os
import csv
from datetime import date,timedelta
import time
import codecs
import matplotlib.pyplot as plt
from matplotlib.pyplot import savefig

import sys
reload(sys)
sys.setdefaultencoding("utf-8")

from struct import *

ground_station = {'FEA8557C0292007002737678': u'兴隆', 'FF6865560359399C01B2C914': u'丽江',
                  'FF97D70002FFAA44024BE4C8': u'德令哈', '0022DA5802C2BA44029A68C8': u'南山',
                  '008EAD00032B6E900205C90C': u'阿里'}

def gen_files(dir, extend):
    '''目录下的文件生成器， 返回文件名'''
    filenames = os.listdir(dir)
    for name in filenames:
        if name.endswith(extend):
            new_name = os.path.join(dir, name)
            # print(new_name)
            yield new_name

def gen_getlines(infile):
    # print('gen_getlines',infile)
    f = csv.reader(open(infile, 'r'), delimiter=',')
    # f = open(infile, 'r')
    not_first = 0
    for line in f:
        # str_list = line.decode('GB2312')
        # str_list = str_list.split(',')

        for i in xrange(len(line)):
            line[i] = line[i].decode('GB2312')
        # print(line)
        if(line[2] and not_first):
            yield line
        not_first = 1

def gen_compare_data(lines, outfile, log_wr):
    instruction_count = 0
    time_pre = date.today()
    del_time = date.today()
    ground_name = ""
    datas = []
    CurveDataAll = ""
    for row in lines:
        # print(row)
        gen_filters_atp(row, log_wr)
        gen_filters(row, u'开始量子通信')
        gen_filters(row, u'停止量子通信')

        if (instruction_count > 0):
            time_cur = time.mktime(time.strptime(row[1], "%Y/%m/%d %H:%M:%S"))
            del_time = time_cur - time_pre
        time_pre = time.mktime(time.strptime(row[1], "%Y/%m/%d %H:%M:%S"))
        row[1] = str(del_time)
        row[0] = ""
        instruction_count = instruction_count + 1
        datas.append(row)

        if del_time == 0:
            log_wr.write(u'指令时间间隔为0\n')

        idx = row[2].find(u'地面站位置：')
        if (idx >= 0):
            station_str = row[2][idx:idx + 36]
            print(u"地面站位置：" + str(idx))
            log_wr.write(station_str + '\t')
            station_code = row[2][idx + 6:idx + 30]
            print(station_code)
            if station_code in ground_station:  # ground_station.has_key(station_code):
                log_wr.write(ground_station[station_code] + '\n')
                ground_name = ground_station[station_code]
            else:
                log_wr.write(u'没有站点对应' + '\n')
                CurveDataAll += gen_filter_curve(row, log_wr)

    curve_data_process(CurveDataAll, outfile + ground_name, log_wr)

    result_file = outfile + ground_name + u'待比较.csv'
    f  = csv.writer(codecs.open(result_file, 'wU', 'utf-16'))
    for item in datas:
        f.writerow(item)
    log_wr.write(u'事件个数：' + str((instruction_count)) + '\n')

def gen_filters(row, pattren):
    idx = row[2].find(pattren)
    if (idx > 0):
        # 获取时间
        end_pos = row[0].find(u'秒0000')
        com_time = row[0][:end_pos]
        # 分离天与其他时间
        tt_time = com_time.split(u'天')
        # print(row)
        tt3 = time.strptime(tt_time[1], "%H:%M:%S")
        tt4 = tt3.tm_hour * 3600 + tt3.tm_min * 60 + tt3.tm_sec
        second_tt = int(tt_time[0]) * 24 * 3600 + tt4

        return row[1], com_time, second_tt
    return None
    # log_wr.write(u"通信开始时间：" + row[1] + '\n' + u'执行时间:' + com_time + u"转换后的秒值：" + str(second_tt) + u"差值：" + str(second_tt - seconds) + '\n')

def gen_filters_atp(row, log_wr):
    # print(row)
    idx = row[2].find(u'精跟瞄X轴跟踪中心')
    if(idx > 0):
        log_wr.write(row[2][idx:idx+50]+'\n')
        print(row[2][idx:idx+50]+'\n')

def gen_filter_curve(row, log_wr):
    '''开始做曲线反演
       首先提取出来曲线里面所有有效字符串,
       然后每16个字符转换为8个字节(方位\俯仰\超前x\超前y)
       将转换完的字节存放至 曲线反演.csv中。'''
    curve_data = ""
    idx = row[2].find(u'注入序号N：')
    if (idx > 0):
        idy = row[2].find(u'注入序号N：01')
        if (idy > 0):
            tt = row[2].find(u'工作曲线数据：')
            curve_time = row[2][tt + 7:tt + 19]
            print(u"曲线时间：" + curve_time)
            seconds = eval('0x' + curve_time[0:8])
            print(seconds)
            log_wr.write(u"曲线时间源码：" + curve_time + u"转换后的秒值：" + str(seconds) + '\n')

            curve_data = row[2][tt + 23:tt + 23 + 84]
            # print u"第一行曲线"+curve_data
        else:
            tt = row[2].find(u'工作曲线数据：')
            curve_data = row[2][tt + 7:tt + 7 + 100]
            # print u"后续曲线"+curve_data
    return curve_data

def curve_data_process(CurveDataAll, file_head,log_wr):
    # print u"所有曲线重新打印"+CurveDataAll
    repeat = len(CurveDataAll) / 4
    # CurveDataAll = pack('1184s', CurveDataAll)
    # print(repeat)
    data = []
    div_data = [182.044, 182.044, 32.00, 32.00]
    courve_filename = file_head + u"_曲线.csv"
    # courvefd = open(courve_filename, 'w')
    courvefd = csv.writer(codecs.open(courve_filename, 'wU', 'utf-16'), delimiter='\t')
    # courvefd = csv.writer(open(courve_filename, 'w'), delimiter=',', lineterminator='\n')
    names = [u'序号', u'粗跟踪方位角', u'粗跟踪俯仰角', u'X轴超前瞄准角', u'Y轴超前瞄准角']
    data_row = [u'序号', u'粗跟踪方位角', u'粗跟踪俯仰角', u'X轴超前瞄准角', u'Y轴超前瞄准角']
    courvefd.writerow(names)
    # courvefd.writerow(u'序号,'+names[0]+','+names[1]+','+names[2]+','+names[3]+'\n')
    # courvefd.writerow('1,')
    for ii in range(0, repeat):
        # print ii
        dd = int(CurveDataAll[ii * 4:ii * 4 + 4], 16)
        if ((dd & 0x8000) == 0x8000):
            dd = (dd - 65536)
        ff = dd / div_data[ii % 4]
        data.append(ff)
        data_row[(ii % 4) + 1] = str(ff)
        # courvefd.writerow(str(ff))
        if (ii % 4 == 3):
            data_row[0] = str(ii / 4 + 2)
            courvefd.writerow(data_row)
    # courvefd.close()


    ##方位\俯仰\超前x\超前y
    fangwei = data[::4]
    fuyang = data[1::4]
    chaoqianx = data[2::4]
    chaoqiany = data[3::4]

    if (len(fangwei) > 0):
        max_angel = max(fangwei)
        min_angel = min(fangwei)
        print(max_angel, min_angel)
        log_wr.write(u'方位角最大值：' + str(max_angel) + u'方位角最小值' + str(min_angel) + '\n')
        max_angel = max(fuyang)
        min_angel = min(fuyang)
        print(max_angel, min_angel)
        log_wr.write(u'俯仰角最大值：' + str(max_angel) + u'俯仰角最小值' + str(min_angel) + '\n')
        # fig_filename = file_head+ground_name+names[1]+".png"
        plt.plot(fangwei)

        plt.plot(fuyang)
        fig_filename = file_head + names[1] + names[2] + ".png"
        savefig(fig_filename)
        plt.clf()
        plt.close()
        plt.plot(chaoqianx)
        plt.plot(chaoqiany)
        fig_filename = file_head + names[3] + names[4] + ".png"
        savefig(fig_filename)
        plt.clf()
        plt.close()
    else:
        log_wr.write(u'无方位俯仰数据' + '\n')
        print(u'无方位俯仰数据' + '\n')

    instruction_count = 0
    datas = []
    CurveDataAll = ''
    log_wr.write(u'-------------------------------------------------------\n')


def zip_files(file_date_dir):
    find_dir = u'\\\\192.168.5.154/量子分系统载荷跟瞄曲线/'

    def find_atp_curve(dir_name):
        aa = os.listdir(dir_name)
        bb = aa[-6:-1]
        for aaa in bb:
            print(aaa + '-------')
        return bb

    import zipfile
    def zip_dir(dir_name, zipfile_name):
        file_list = []
        if (os.path.isfile(dir_name)):
            if (dir_name.endswith('.xls') == False):
                print(dir_name)
                file_list.append(dir_name)
        else:
            for root, dirs, files in os.walk(dir_name):
                for name in files:
                    if (name.endswith('.xls') == False):
                        file_list.append(os.path.join(root, name))
        zf = zipfile.ZipFile(zipfile_name, 'w', zipfile.zlib.DEFLATED)
        dirs = find_atp_curve(find_dir)
        for s_dir in dirs:
            files = os.listdir(find_dir + s_dir)

            for idx, names in enumerate(files):
                # print(names)
                flt = names.endswith('.epm') or dir_name.startswith('89度') or dir_name.startswith('G2000')
                if flt == False:
                    file_list.append(find_dir + s_dir + '/' + names)

        for tar in file_list:
            arcname = tar[len(dir_name):]
            zf.write(tar, arcname)
        zf.close()

    zipfile_name = file_date_dir + '.zip'
    zip_dir(file_date_dir, zipfile_name)

if __name__== "__main__":

    #1. 指定工作目录
    # 处理后的文件的压缩包也放在该目录下
    print('start')
    file_dir = u'D:/tt'
    #2. 获取今天的日期, 文件是放在今天的日期的文件夹下的
    folder = '20170329'#time.strftime("%Y%m%d", time.gmtime())

    # 3. 获取文件夹下的文件列表
    file_date_dir = os.path.join(file_dir, folder)
    # print(file_date_dir)
    files = gen_files(file_date_dir, ".xls")

    # log文件
    log_filename = os.path.join(file_date_dir,folder) + u'待比较.log'  # file_head+u'待比较.log'
    log_wr = open(log_filename, 'w')

    file_num = 0
    for file_name in files:
        print('files to be processed:', file_name)
        # 获取文件中的行
        lines = gen_getlines(file_name)

        # 文件头
        file_head = os.path.splitext(file_name)[0]


        # 结果文件
        result_file = file_head + str(file_num)

        gen_compare_data(lines, result_file, log_wr)

    # print(file_date_dir)
    # log_wr.write(u"zip directory:" + file_date_dir)
    log_wr.close()

    # zip_files(file_date_dir)
    print(u'end')







