import matplotlib.pyplot as plt
import math
import random
import numpy as np

import scipy.signal

# plt.subplot(4,1,1)
# t = np.arange(0,8, 0.001)
# d = np.array([[0,0],[0.5,1],[1,1],[1.5,0],[2,1],[2.5,1],[3,0],[3.5,0],[4,0],[4.5,1],[5,1],[5.5,0],[6,1],[6.5,1],[7,0],[7.5,0]])
# plt.plot(t, d)
# plt.show()

import time
start = time.time()
N = 40 ##每周期多少个点
fs = 1
phi = 1/8 * math.pi #起始相位
s_n = [(2*math.pi*fs*t)/N  + phi  for t in range(N)]    # 生成了一个周期的点

repeat = 10  #重复多少个周期
n = s_n * 10
end = time.time()

print(end - start)

fs = 2 #采样率(G)
axis_x = np.linspace(0,len(n)/fs,num=len(n))
  
#频率为5Hz的正弦信号  
x = [math.sin(i) for i in n]  
# plt.subplot(221)
title = str(2e9/N)+u'Hz的正弦信号'
plt.plot(axis_x,x)
plt.title(title)
plt.axis('tight')

  
# #频率为5Hz、幅值为3的正弦+噪声
# x1 = [random.gauss(0,0.5) for i in range(N)]
# xx = []
# #有没有直接两个列表对应项相加的方式？？
# for i in range(len(x)):
#     xx.append(x[i]*3 + x1[i])
#
# plt.subplot(222)
# plt.plot(axis_x,xx)
# plt.title(u'频率为5Hz、幅值为3的正弦+噪声')
# plt.axis('tight')
#
# #频谱绘制
# xf = np.fft.fft(x)
# xf_abs = np.fft.fftshift(abs(xf))
# axis_xf = np.linspace(-N/2,N/2-1,num=N)
# plt.subplot(223)
# plt.title(u'频率为5Hz的正弦频谱图')
# plt.plot(axis_xf,xf_abs)
# plt.axis('tight')
#
# #频谱绘制
# xf = np.fft.fft(xx)
# xf_abs = np.fft.fftshift(abs(xf))
# plt.subplot(224)
# plt.title(u'频率为5Hz的正弦频谱图')
# plt.plot(axis_xf,xf_abs)
# plt.axis('tight')
  
plt.show()  