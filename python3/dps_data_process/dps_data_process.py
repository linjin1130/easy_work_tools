import csv
import os
import scipy

import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

import matplotlib.mlab as mlab
import pandas as pd


filename = 'D:\\python\\easy_work_tools\\python3\\dps_data_process\\6.csv'
filename_wr = 'D:\\python\\easy_work_tools\\python3\\dps_data_process\\process_6.csv'


# 定义一个求t分布的置信区间函数
def ci_t(data, confidence=0.95):
    # 先求一下 bins ,以便画图用得上.
    IQR = data.quantile(0.75) - data.quantile(0.25)
    bin_size = 2 * IQR / len(data) ** (1.0 / 3)

    # 画个源数据图表.以便对源数据的一个直观了解
    plt.rcParams['font.sans-serif'] = ['SimHei']
    n = plt.hist(data, bins=round(bin_size), rwidth=0.9)
    plt.vlines(data.mean(), 0, max(n[0]) + 1, colors="r", linestyles="dashed", label="平均值%.2f" % np.mean(data))
    plt.title('源数据' + str(len(data)) + '个样本分布 直方图')
    plt.ylabel('频数')
    plt.legend()
    plt.show()

    # 真正开始计算
    sample_mean = np.mean(data)
    sample_std = np.std(data)
    sample_size = len(data)
    alpha = 1 - confidence
    t_score = scipy.stats.t.isf(alpha / 2, df=(sample_size - 1))

    ME = t_score * sample_std / np.sqrt(sample_size)
    lower_limit = sample_mean - ME
    upper_limit = sample_mean + ME

    print(str(confidence * 100) + '%% Confidence Interval: ( %.2f, %.2f)' % (lower_limit, upper_limit))
    return lower_limit, upper_limit



new_list = []
exclude_lst = [1,8,28,41,61,95,127]
with open(filename) as f:
    reader = csv.reader(f)
    raw_data = list(reader)
    poc_dic = { }
    first = 1
    # 按poc编号为字典键值，APD2，APD1计数列表为value建立字典
    for row in raw_data[1:]:
        if row[0] not in poc_dic.keys():
            poc_dic[row[0]] = [[],[]]
        poc_dic[row[0]][0].append(int(row[-2]))
        poc_dic[row[0]][1].append(int(row[-1]))

    # 准备计算每个poc的APD2列表的筛选阈值，最小值
    # 筛选依据：小值（APD2）众数的值*2
    poc_th_list = [0 for i in range(128)]
    min_val = [0 for i in range(128)]
    for key in poc_dic.keys():
        # print(poc_dic[key][1])
        data_num = len(poc_dic[key][1])
        print(f'poc:{key},{data_num}')
        max_cnt = stats.mode(poc_dic[key][1])[0][0]
        counts = stats.mode(poc_dic[key][1])[1][0]
        # 返回众数
        # max_cnt = np.argmax(counts)
        print(f'众数：{max_cnt},值：{counts}')
        # 数据过滤
        th = max_cnt*3
        poc_th_list[int(key)] = th


        #得到新的list, 求西格玛值和95%置信区间的下限
        new_l = []
        for item in poc_dic[key][1]:
            if item < th:
                new_l.append(item)
        # y = mlab.normpdf(10, np.mean(new_l), np.std(new_l))  # 拟合一条最佳正态分布曲线y
        # plt.figure()
        # plt.hist(new_l, 10, normed=1, facecolor='blue', alpha=0.5)
        # # plt.plot(10, y, 'r--')  # 绘制y的曲线
        # plt.show()

        SE = np.std(new_l)#/np.sqrt(len(new_l))
        aa = stats.norm.interval(0.95, loc=np.mean(new_l), scale=SE)
        # print(aa)
        if(aa[0]) < 0:
            dark_cnt = 0
        else:
            dark_cnt = int(round(aa[0]))
        print(dark_cnt)
        min_val[int(key)] = dark_cnt
        # nn = pd.DataFrame(new_l)
        # nn = nn/max(new_l)
        # plt.figure()
        # plt.plot(nn)
        # plt.show()
        # print('sss')
        # print(nn.quantile(0.75))
        # print('aaaa')
        # print(nn.quantile(0.25))
        #
        # print(nn.quantile(0.75) - nn.quantile(0.25))
        # print(ci_t(nn, 0.95))

        # rm_list = []
        # for idx,item in enumerate(poc_dic[key][1]):
        #
        #     if item > th:
        #         rm_list.append(idx)
        #         # print(item)
        # rm_list.reverse()
        # for idx in rm_list:
        #     poc_dic[key][0].remove(poc_dic[key][0][idx])
        #     poc_dic[key][1].remove(poc_dic[key][1][idx])
        # print(len(poc_dic[key][1]))

        # for idx,item in enumerate(poc_dic[key][1]):
        #     poc_dic[key][0][idx] -= min_val
        #     poc_dic[key][1][idx] -= min_val
        # arr0 = np.asarray(poc_dic[key][0])
        # arr1 = np.asarray(poc_dic[key][1])
        # visibility = np.mean((arr0-arr1)/(arr0+arr1))
        # print(visibility)
        # total_vis.append(visibility)
    # 将排除列表的下限设为0
    for poc_num in exclude_lst:
        min_val[poc_num] = 0

    # 建立新的列表

    new_list.append(raw_data[0])
    for data in raw_data[1:]:
        # 减掉暗计数
        # print(data[-1], min_val[int(data[0])])
        if int(data[-1]) > min_val[int(data[0])]:
        # if int(data[-1]) < poc_th_list[int(data[0])]:
            temp_str = int(data[-1]) - min_val[int(data[0])]
            data[-1] = str(temp_str)
            temp_str = int(data[-2]) - min_val[int(data[0])]
            data[-2] = str(temp_str)
        new_list.append(data)
# fd = os.open(filename_wr, 0)
# os.close(fd)
with open(filename_wr, 'w', newline="") as f:
    csvwriter = csv.writer(f)
    csvwriter.writerows(new_list)