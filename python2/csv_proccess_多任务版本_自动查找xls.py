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

ground_station = {'FEA8557C0292007002737678': u'��¡', 'FF6865560359399C01B2C914': u'����',
                  'FF97D70002FFAA44024BE4C8': u'�����', '0022DA5802C2BA44029A68C8': u'��ɽ',
                  '008EAD00032B6E900205C90C': u'����'}

def gen_files(dir, extend):
    '''Ŀ¼�µ��ļ��������� �����ļ���'''
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
        gen_filters(row, u'��ʼ����ͨ��')
        gen_filters(row, u'ֹͣ����ͨ��')

        if (instruction_count > 0):
            time_cur = time.mktime(time.strptime(row[1], "%Y/%m/%d %H:%M:%S"))
            del_time = time_cur - time_pre
        time_pre = time.mktime(time.strptime(row[1], "%Y/%m/%d %H:%M:%S"))
        row[1] = str(del_time)
        row[0] = ""
        instruction_count = instruction_count + 1
        datas.append(row)

        if del_time == 0:
            log_wr.write(u'ָ��ʱ����Ϊ0\n')

        idx = row[2].find(u'����վλ�ã�')
        if (idx >= 0):
            station_str = row[2][idx:idx + 36]
            print(u"����վλ�ã�" + str(idx))
            log_wr.write(station_str + '\t')
            station_code = row[2][idx + 6:idx + 30]
            print(station_code)
            if station_code in ground_station:  # ground_station.has_key(station_code):
                log_wr.write(ground_station[station_code] + '\n')
                ground_name = ground_station[station_code]
            else:
                log_wr.write(u'û��վ���Ӧ' + '\n')
                CurveDataAll += gen_filter_curve(row, log_wr)

    curve_data_process(CurveDataAll, outfile + ground_name, log_wr)

    result_file = outfile + ground_name + u'���Ƚ�.csv'
    f  = csv.writer(codecs.open(result_file, 'wU', 'utf-16'))
    for item in datas:
        f.writerow(item)
    log_wr.write(u'�¼�������' + str((instruction_count)) + '\n')

def gen_filters(row, pattren):
    idx = row[2].find(pattren)
    if (idx > 0):
        # ��ȡʱ��
        end_pos = row[0].find(u'��0000')
        com_time = row[0][:end_pos]
        # ������������ʱ��
        tt_time = com_time.split(u'��')
        # print(row)
        tt3 = time.strptime(tt_time[1], "%H:%M:%S")
        tt4 = tt3.tm_hour * 3600 + tt3.tm_min * 60 + tt3.tm_sec
        second_tt = int(tt_time[0]) * 24 * 3600 + tt4

        return row[1], com_time, second_tt
    return None
    # log_wr.write(u"ͨ�ſ�ʼʱ�䣺" + row[1] + '\n' + u'ִ��ʱ��:' + com_time + u"ת�������ֵ��" + str(second_tt) + u"��ֵ��" + str(second_tt - seconds) + '\n')

def gen_filters_atp(row, log_wr):
    # print(row)
    idx = row[2].find(u'������X���������')
    if(idx > 0):
        log_wr.write(row[2][idx:idx+50]+'\n')
        print(row[2][idx:idx+50]+'\n')

def gen_filter_curve(row, log_wr):
    '''��ʼ�����߷���
       ������ȡ������������������Ч�ַ���,
       Ȼ��ÿ16���ַ�ת��Ϊ8���ֽ�(��λ\����\��ǰx\��ǰy)
       ��ת������ֽڴ���� ���߷���.csv�С�'''
    curve_data = ""
    idx = row[2].find(u'ע�����N��')
    if (idx > 0):
        idy = row[2].find(u'ע�����N��01')
        if (idy > 0):
            tt = row[2].find(u'�����������ݣ�')
            curve_time = row[2][tt + 7:tt + 19]
            print(u"����ʱ�䣺" + curve_time)
            seconds = eval('0x' + curve_time[0:8])
            print(seconds)
            log_wr.write(u"����ʱ��Դ�룺" + curve_time + u"ת�������ֵ��" + str(seconds) + '\n')

            curve_data = row[2][tt + 23:tt + 23 + 84]
            # print u"��һ������"+curve_data
        else:
            tt = row[2].find(u'�����������ݣ�')
            curve_data = row[2][tt + 7:tt + 7 + 100]
            # print u"��������"+curve_data
    return curve_data

def curve_data_process(CurveDataAll, file_head,log_wr):
    # print u"�����������´�ӡ"+CurveDataAll
    repeat = len(CurveDataAll) / 4
    # CurveDataAll = pack('1184s', CurveDataAll)
    # print(repeat)
    data = []
    div_data = [182.044, 182.044, 32.00, 32.00]
    courve_filename = file_head + u"_����.csv"
    # courvefd = open(courve_filename, 'w')
    courvefd = csv.writer(codecs.open(courve_filename, 'wU', 'utf-16'), delimiter='\t')
    # courvefd = csv.writer(open(courve_filename, 'w'), delimiter=',', lineterminator='\n')
    names = [u'���', u'�ָ��ٷ�λ��', u'�ָ��ٸ�����', u'X�ᳬǰ��׼��', u'Y�ᳬǰ��׼��']
    data_row = [u'���', u'�ָ��ٷ�λ��', u'�ָ��ٸ�����', u'X�ᳬǰ��׼��', u'Y�ᳬǰ��׼��']
    courvefd.writerow(names)
    # courvefd.writerow(u'���,'+names[0]+','+names[1]+','+names[2]+','+names[3]+'\n')
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


    ##��λ\����\��ǰx\��ǰy
    fangwei = data[::4]
    fuyang = data[1::4]
    chaoqianx = data[2::4]
    chaoqiany = data[3::4]

    if (len(fangwei) > 0):
        max_angel = max(fangwei)
        min_angel = min(fangwei)
        print(max_angel, min_angel)
        log_wr.write(u'��λ�����ֵ��' + str(max_angel) + u'��λ����Сֵ' + str(min_angel) + '\n')
        max_angel = max(fuyang)
        min_angel = min(fuyang)
        print(max_angel, min_angel)
        log_wr.write(u'���������ֵ��' + str(max_angel) + u'��������Сֵ' + str(min_angel) + '\n')
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
        log_wr.write(u'�޷�λ��������' + '\n')
        print(u'�޷�λ��������' + '\n')

    instruction_count = 0
    datas = []
    CurveDataAll = ''
    log_wr.write(u'-------------------------------------------------------\n')


def zip_files(file_date_dir):
    find_dir = u'\\\\192.168.5.154/���ӷ�ϵͳ�غɸ�������/'

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
                flt = names.endswith('.epm') or dir_name.startswith('89��') or dir_name.startswith('G2000')
                if flt == False:
                    file_list.append(find_dir + s_dir + '/' + names)

        for tar in file_list:
            arcname = tar[len(dir_name):]
            zf.write(tar, arcname)
        zf.close()

    zipfile_name = file_date_dir + '.zip'
    zip_dir(file_date_dir, zipfile_name)

if __name__== "__main__":

    #1. ָ������Ŀ¼
    # �������ļ���ѹ����Ҳ���ڸ�Ŀ¼��
    print('start')
    file_dir = u'D:/tt'
    #2. ��ȡ���������, �ļ��Ƿ��ڽ�������ڵ��ļ����µ�
    folder = '20170329'#time.strftime("%Y%m%d", time.gmtime())

    # 3. ��ȡ�ļ����µ��ļ��б�
    file_date_dir = os.path.join(file_dir, folder)
    # print(file_date_dir)
    files = gen_files(file_date_dir, ".xls")

    # log�ļ�
    log_filename = os.path.join(file_date_dir,folder) + u'���Ƚ�.log'  # file_head+u'���Ƚ�.log'
    log_wr = open(log_filename, 'w')

    file_num = 0
    for file_name in files:
        print('files to be processed:', file_name)
        # ��ȡ�ļ��е���
        lines = gen_getlines(file_name)

        # �ļ�ͷ
        file_head = os.path.splitext(file_name)[0]


        # ����ļ�
        result_file = file_head + str(file_num)

        gen_compare_data(lines, result_file, log_wr)

    # print(file_date_dir)
    # log_wr.write(u"zip directory:" + file_date_dir)
    log_wr.close()

    # zip_files(file_date_dir)
    print(u'end')







