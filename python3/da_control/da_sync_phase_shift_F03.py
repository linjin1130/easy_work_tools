from DAboard import *
import time
import matplotlib.pyplot as plt
da = DABoard()
da2 = DABoard()

adname = 'B17-R_21.35m-'
# new_ip = '10.0.2.7'
da2_ip = '10.0.5.3'
# board_status = da.connect(new_ip)
board_status2 = da2.connect(da2_ip)
# da.GetFlashType()   B`
# da.DA_reset()
cnt_arr = []
err_cnt = []
pre = 1000
start_pos = 0
temp_start_pos = 0
stop_pos = 0
for i in range(0,100):
    da2.setDAADPLLDelay(0)
    time.sleep(0.01)
    cnt0 = da2.GetDAADSyncErrCnt()
    time.sleep(0.01)
    cnt = da2.GetDAADSyncErrCnt()
    cnt_arr.append(i)
    delta = 0
    if cnt < cnt0:
        delta = cnt+0x00100000000 - cnt0
    else:
        delta = cnt - cnt0
    err_cnt.append(delta)
    print(i, delta, cnt, cnt0)

    if delta < 11 and pre > 10:
        temp_start_pos = i
    if delta > 10 and pre < 11:
        print(i, temp_start_pos)
        if  (i-temp_start_pos > 20):
            stop_pos = i
            start_pos = temp_start_pos
    pre = delta

print(start_pos,stop_pos)
for i in range(100-stop_pos+int((stop_pos-start_pos)/2)):
    da2.setDAADPLLDelay(1)

plt.figure()
plt.xlabel(u"相位调节次数")
plt.ylabel(u'同步错误计数(对数)')
plt.title(adname+da2_ip+u"同步延时调节计数")
plt.semilogy()
plt.plot(err_cnt)
plt.show()

# da.DA_reprog()
da.disconnect()
da2.disconnect()