def get_mac_ifc_num():
    # 1. 执行命令读取ARP信息
    # 2. 在信息中取得内网对应的MAC口编号
    # 3. 根据编号进入到ARP和DA boards key的生成

    # import os
    import subprocess
    MAC_num = -1
    cmd = 'cmd.exe /c arp_info.bat'

    p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

    curline = p.stdout.readline()

    while (curline != b''):
        str_info = str(curline, encoding="gbk")
        # print(str_info)
        if str_info.find('10.0.') > 0:
            # print(str_info)
            MAC_num = int(str_info.split('---')[1].strip(), 16)
            print(MAC_num)
            break
        curline = p.stdout.readline()

    p.wait()
    if int(MAC_num) < 0:
        print('注意：本机没有内网地址')
    return MAC_num


import itertools
import os
#获取待运行主机的内网地址对应的mac编号
mac_num = get_mac_ifc_num()

mixerZeros = '#mxrZeros_170706T132236_'

work_dir = os.getcwd()#'F:\\PycharmProjects\\easy_work_tools\\python3\\DA_Key\\tset'
# print(work_dir)
#每个列表的第一个元素代表该套系统中的主板，生成的文件也以该板号做后缀命名
da_board_list1 = ['C05', 'D13', 'D09', 'D17', 'D01']
da_board_list2 = ['E09', 'E08', 'E30', 'E26', 'E31']
da_board_list3 = ['E24','E14','E29','D21','C11','B08','B05','D16','E03','E32','E11','D15','E06']
da_board_list4 = ['E10','C08','C03','E16','E17','E18','E19','D08','D02','E12','E13','C09','E07','D05','D06','E04']

#该列表表明想对哪几套系统生成参数配置文件
da_brd_list = [da_board_list4]

def set_check(set1, set2):
    #检查两个列表是否有重复
    if len(set1 & set2) > 0:
        print('有重复：', set1 & set2)

pos = ['right', 'left']



for lst in da_brd_list:
    #检查列表内部是否有重复
    if len(lst) > len(set(lst)):
        print('有重复', lst)

for item in itertools.permutations(da_brd_list, 2):
    #检查任意两个列表是否有重复
    set_check(set(item[0]), set(item[1]))

#待生成ARP表的bat文件
f_arp = open(os.path.join(work_dir,"arp_gen.bat"), 'w')
f_ping = open(os.path.join(work_dir,"ping_gen.bat"), 'w')

out_file = 'ping_output.txt'
f_ping.write('echo start ping >'+out_file+'\n')

#读取参数列表
para_list = []
para_f = open(os.path.join(work_dir,'da_para.txt'), 'r')
lines = para_f.readlines()
dic = {}
for line in lines:
    line = line.strip('\n')
    t_key = line.split(':')[0]
    dic[t_key] = line.split(':')[1:]

# for key in dic:
#     print(dic[key])
#板号与序号的对应关系字典
# seg_dic = {'A':[1,0], 'B':[1,100], 'C':[2,0], 'D':[3,0], 'E':[4,0], 'F':[5,0], 'G':[6,0], 'H':[7,0], 'I':[8,0], 'J':[9,0]}

list1 = 'ABCDEFGHIJKLMN'
list2 = [1,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
list3 = [0,100,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
seg_dic = dict(zip(list1[:10], list(zip(list2[:10], list3[:10]))))
# print(seg_dic)

#根据板号获取IP地址
def get_ip(str_in):
    return '10.0.'+str(seg_dic[str_in[0]][0])+'.'+str(seg_dic[str_in[0]][1] + int(str_in[1:]))+''

#根据板号获取MAC地址
def get_mac(str_in):
    str_seg = hex(seg_dic[str_in[0]][0])[2:]
    if len(str_seg) == 1:
        str_seg = '0'+ str_seg

    num = seg_dic[str_in[0]][1] + int(str_in[1:])
    str_num = hex(num)[2:]
    if len(str_num) == 1:
        str_num = '0' + str_num
    return '00-0a-35-00-'+str_seg+'-'+str_num+''

#生成da 配置参数， f_name:文件名， da_list:该套系统所包含的DA板
def gen_key(f_name, da_list):
    f = open(os.path.join(work_dir,f_name), 'w')

    f.write('// DAC boards\n')
    f.write('{\n')
    f.write('\t"da_boards":\n')
    f.write('\t\t[\n')
    i = 1

    gain_default = '[511, 511, 511, 511]'
    offset_default = '[-200, -200, -200, -200]'

    # print(dic.keys())

    for da in da_list:
        # print(da)
        arp_cmd = "netsh -c i i add neighbors " + str(mac_num) + ' ' + get_ip(da) + ' ' + get_mac(da) + '\n'
        ping_cmd = 'ping -n 1 '+ get_ip(da) + ' >>' + out_file + '\n'
        f_ping.write(ping_cmd)
        f_arp.write(arp_cmd)
        if da in dic.keys():
            gain = dic[da][0]
            offset = dic[da][1]
        else:
            gain = gain_default
            offset = offset_default
        da_pos = pos[i%2]
        f.write('\t\t\t{\t"name":\t\t\t\t"'+da+'",\t\t\t\t\t\t // rack '+str(i)+', '+da_pos+'\n')
        f.write('\t\t\t \t"ip":\t\t\t\t"'+get_ip(da)+'",\n')
        f.write('\t\t\t \t"port":\t\t\t\t80,\n')
        f.write('\t\t\t \t"numChnls":\t\t\t4,\t\t\t\t\t\t\t// number of channels\n')
        f.write('\t\t\t \t"samplingRate":\t\t2e9,\t\t\t\t\t\t// sampling rate\n')
        f.write('\t\t\t \t"daTrigDelayOffset":460,\n')
        f.write('\t\t\t \t"syncDelay":\t\t0,\n')
        f.write('\t\t\t \t"gain":\t\t\t\t'+gain+',\n')
        f.write('\t\t\t \t"offsetCorr":\t\t'+offset+',\n')
        f.write('\t\t\t \t"mixerZeros":\t\t["'+mixerZeros+'",\n')
        f.write('\t\t\t \t\t\t\t\t\t"'+mixerZeros+'",\n')
        f.write('\t\t\t \t\t\t\t\t\t"'+mixerZeros+'",\n')
        f.write('\t\t\t \t\t\t\t\t\t"'+mixerZeros+'"]\n')

        if i==len(da_list):
            f.write('\t\t\t}\n')
        else:
            f.write('\t\t\t},\n')
        i += 1

    f.write('\t\t]\n')
    f.write('}\n')
    f.close()

for ff in da_brd_list:
    gen_key('da_boards-'+ ff[0] + '.key', ff)

f_arp.close()
f_ping.close()
print('完成')