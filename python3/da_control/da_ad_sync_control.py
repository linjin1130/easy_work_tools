from DAboard import *
import time
import matplotlib.pyplot as plt
da = DABoard()
da2 = DABoard()
# new_ip = '10.0.2.7'
da2_ip = '10.0.5.5'
# board_status = da.connect(new_ip)
board_status2 = da2.connect(da2_ip)
# da.GetFlashType()
# da.DA_reset()
cnt_arr = []
err_cnt = []
pre = 0
for i in range(0,104):
    da2.setDAADSyncDelay(i*5)
    time.sleep(1)
    for j in range(4):
        time.sleep(2)
        cnt_arr.append(i)
        cnt = da2.GetDAADSyncErrCnt()
        # delta = (cnt+0x100000000 - pre) % 0xFFFFFFF
        # pre = cnt
        print(cnt)
        err_cnt.append(cnt)
    print(i)
# plt.figure()
# plt.plot(cnt_arr,err_cnt)
# plt.show()

fig = plt.figure()

ax1 = fig.add_subplot(111)
ax1.plot(cnt_arr)
ax1.set_ylabel('Y values for exp(-x)')
ax1.set_title("Double Y axis")

ax2 = ax1.twinx()  # this is the important function
ax2.plot(err_cnt, 'r')
ax2.set_ylabel('Y values for ln(x)')
ax2.set_xlabel('Same X for both exp(-x) and ln(x)')

plt.show()
# da.DA_reprog()
da.disconnect()
da2.disconnect()