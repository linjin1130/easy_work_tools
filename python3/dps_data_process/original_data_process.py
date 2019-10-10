
import os
import csv
import matplotlib.pyplot as plt
import numpy as np

files = os.listdir('数据')
print(len(files))
print(files)
def visibility_process(data_dic):
    vis = [0]*128
    # print(data_dic['0'][1])
    for key in data_dic.keys():
        avg_large = np.mean(np.asarray(data_dic[key][0])/np.asarray(data_dic[key][1]))
        a_1 = np.asarray(data_dic[key][0]) - np.asarray(data_dic[key][1])
        a_2 = np.asarray(data_dic[key][0]) + np.asarray(data_dic[key][1])
        avg = a_1 / a_2
        # avg_min = np.mean(np.asarray(data_dic[key][1]))
        # if avg_min > avg_large:
        #     avg_min, avg_large = avg_large, avg_min
        # vis.append((avg_large - avg_min )/(avg_large+avg_min))

        vis[int(key)] =np.mean(avg)
    return vis

expact_val = [0.990881128,0.984090432,  0.979084605,0.97840538,0.973991732,0.953741157,0.945469978,0.926783103]
def draw_visibility(f_name, vis, filted, val):
    # print(filted)
    plt.figure()
    plt.subplot(211)
    plt.title(f_name)
    plt.plot(vis)
    plt.subplot(212)
    plt.plot(filted)
    plt.plot(expact_val)
    plt.xlabel(f'大于0.96的poc数{val}')
    # plt.show()
    plt.savefig('结果/'+f_name+'.png')
    plt.close()

def get_vis_bigger_than_96(vis):
    cnt = 0
    for i in vis:
        if i >= 0.96:
           cnt += 1
    return cnt

def get_similarity(vis):
    filter_poc = [1,8,28,41,61,87, 95,127]
    filted = []

    for idx, poc_num in enumerate(filter_poc):
        if(poc_num > len(vis)):
            break
        filted.append(vis[poc_num])
    return filted

p_cnt = 0
for f_name in files:
    p_cnt += 1
    with open('数据/'+f_name, 'r') as csv_file:
        s_f = csv.reader(csv_file)
        data_large = []
        data_min = []
        poc = []
        data_dic = {}
        poc_num = 0
        for line in s_f:
            if line[1] == '23':
                # print(data_dic.keys())
                poc_num += 1
                poc_num %= 128
                if str(poc_num) in data_dic.keys():
                    data_dic[str(poc_num)][0].append(int(line[3]))
                    data_dic[str(poc_num)][1].append(int(line[4]))
                else:
                    data_dic[str(poc_num)]=[[int(line[3])],[int(line[4])]]
        print(data_dic.keys())

        visibility = visibility_process(data_dic)
        print(p_cnt, f_name)
        val = get_vis_bigger_than_96(visibility)
        filted = get_similarity(visibility)

        draw_visibility(f_name[:-4], visibility, filted, val)