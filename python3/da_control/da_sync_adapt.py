from DAboard import *
import time
import matplotlib.pyplot as plt
da1 = DABoard()
da2 = DABoard()

adname = 'B18-R_21.35m-'
da1_ip = '10.0.5.2'
da2_ip = '10.0.5.4'
board_status = da1.connect(da1_ip)
board_status2 = da2.connect(da2_ip)
# da.GetFlashType()   B`
# da.DA_reset()
cnt_arr = []
err_cnt = []
# da.SetIsMaster(0)
# da2.SetIsMaster(1)
# da_ctrl = waveform()
# # da_ctrl.generate_seq()
# da_ctrl.generate_squr()
# da_ctrl.generate_trig_seq(length=len(da_ctrl.wave)>>3)
# print(len(da_ctrl.seq))
# print(len(da_ctrl.wave))
# # print("wave")
#
#
# # plt.figure()
# # plt.plot(da_ctrl.wave)
# # plt.show()
# print(len(da_ctrl.wave))
# da2.SetTrigInterval(200)
# da2.SetTrigCount(100)
# cnt=0
# for i in range(1):
#     da.WriteSeq(1,da_ctrl.seq)
#     da.WriteWave(1,da_ctrl.wave)
#     da.WriteSeq(2,da_ctrl.seq)
#     da.WriteWave(2,da_ctrl.wave)
#     da.WriteSeq(3,da_ctrl.seq)
#     da.WriteWave(3,da_ctrl.wave)
#     da.WriteSeq(4,da_ctrl.seq)
#     da.WriteWave(4,da_ctrl.wave)
#     da2.WriteSeq(1,da_ctrl.seq)
#     da2.WriteWave(1,da_ctrl.wave)
#     da2.WriteSeq(2,da_ctrl.seq)
#     da2.WriteWave(2,da_ctrl.wave)
#     da2.WriteSeq(3,da_ctrl.seq)
#     da2.WriteWave(3,da_ctrl.wave)
#     da2.WriteSeq(4,da_ctrl.seq)
#     da2.WriteWave(4,da_ctrl.wave)
#     cnt+=1
#     print(cnt)
#
#     da.StartStop(240)
#     da2.StartStop(240)
#     da.StartStop(15)
#     da2.StartStop(15)
#     da2.SendIntTrig()
#     time.sleep(1)
# #



da2.SetTrigInterval(200)
da2.SetTrigCount(5000)
da2.setOutputSwitch(0)# switch off
da1.setOutputSwitch(0)# switch off
da2.StartTrigAdapt()
time.sleep(1)
da2.setOutputSwitch(1)# switch off
da1.setOutputSwitch(1)# switch off
# for i in range(600):
#     time.sleep(0.7)
#     cnt = da2.GetDAADSyncErrCnt()
#     cnt_arr.append(cnt)
#     print(cnt)
#
# plt.figure()
# plt.xlabel(u"    xxxxxx")
# plt.ylabel(u'同步错误计数(对数)')
# plt.title(adname+da2_ip+u"同步延时调节计数")
# # plt.semilogy()#对数显示
# plt.plot(cnt_arr)
# plt.show()

# da.DA_reprog()
# da.disconnect()
da2.disconnect()