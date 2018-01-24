import os
import csv
src_dir = 'E:\\工程相关\\超导量子计算\\测试文档\\DA\静态测试记录\\20180122_增益偏置测试'
ftarget = 'da_para.txt'
f_old_para = 'da_para_old.txt'
para = []

name = ''
gain = ''
offset = ''

map_dic = {'1':'A', '2':'C', '3':'D', '4':'E', '5':'F', '6':'G', '7':'H', '8':'I'}

def get_seg(str_in):
    seg = 'B'
    num = '0'
    if int(str_in[0]) == 1 and int(str_in[1]) > 100:
        num = str(int(str_in[1]) - 100)
    else:
        # print(str_in)
        seg = map_dic[str_in[0]]
        num = str_in[1]
    if len(num) == 1:
        num = '0'+num
    return seg+num

def get_name(str_in):
    seg = str_in
    if str_in.find('.') > -1:
        seg = get_seg(str_in.split('.')[2:])
    else:
        if len(str_in) == 2:
            seg = str_in[0] + '0' + str_in[1]
    return seg

names = []

for f in os.listdir(src_dir):
    if f.endswith('csv'):
        with open(os.path.join(src_dir,f), 'r') as csvfile:
            reader = csv.reader(csvfile)
            name = ''
            gain = []
            offset = []
            for line in reader:
                # print(line)
                if line[0].find('测试板号') > -1:
                    # print(line)
                    name = get_name(line[1])
                if line[0].find('增益码值') > -1:
                    gain = '[' + ','.join(line[1:5]) + ']'
                if line[0].find('偏置码值') > -1:
                    offset =  '[' + ','.join(line[1:5]) + ']'
                    para.append([name, gain, offset])
                    names.append(name)
                    break

fw = open(ftarget, 'w')

f_old = open(f_old_para, 'r')
lines = f_old.readlines()
for line in lines:
    line = line.replace('\t', '')
    line = line.replace('\n', '')
    if line.split(':')[0] not in names:
        para.append(line.split(':'))
        # print([line.split(':')])
# new_l = para.sort()
for row in sorted(para):
    # print(':'.join(row))
    print(row)
    fw.write(':'.join(row)+'\n')
fw.close()
