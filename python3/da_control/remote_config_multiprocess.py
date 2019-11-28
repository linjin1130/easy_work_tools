from remote_config import *

import threading
import time

from multiprocessing import Process
condigs1 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_72_30_SPANSION_U.bin'
condigs2 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_72_30_SPANSION_G.bin'


def config_run(ip):
    # V01_69_28_SPANSION_U_SLH_LW
    new_ip = ip
    source_file_name = condigs2
    sucess = 0
    failure = 0
    if da_config_flash(new_ip, source_file_name, erase=True):
        sucess += 1
        print('configure successfull')
    else:
        failure += 1
        print('Error: confugure failed')
    print('成功{0}次，失败{1}次'.format(sucess, failure))

    source_file_name = condigs1

    if da_config_flash(new_ip, source_file_name, erase=False):
        sucess += 1
        print('configure successfull')
    else:
        failure += 1
        print('Error: confugure failed')
    print('成功{0}次，失败{1}次'.format(sucess, failure))



class ConfigProcess(Process):
    def __init__(self,threadID, ip):
        super().__init__()
        self.threadID = threadID
        self.ip = ip

    def run(self):
        _s = time.time()
        print(f"F{self.threadID}开始运行：{_s}")
        config_run(self.ip)
        # da = DABoard()
        # board_status = da.connect(self.ip)
        # print(board_status)
        # da.set_monitor(1)
        # time.sleep(0.5)
        # da.disconnect()
        _t = time.time()
        print(f"F{self.threadID}结束运行：{_t}，耗时：{round(_t - _s, 2)} ")


class ConfigThread(threading.Thread):   #继承父类threading.Thread
    def __init__(self, threadID, ip):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.ip = ip

    def run(self):    #把要执行的代码写到run函数里面，线程在创建后会直接运行run
        _s = time.time()
        print(f"F{self.threadID}开始运行：{_s}")
        config_run(self.ip)
        # da = DABoard()
        # board_status = da.connect(self.ip)
        # print(board_status)
        # da.set_monitor(1)
        # time.sleep(0.5)
        # da.disconnect()
        _t = time.time()
        print(f"F{self.threadID}结束运行：{_t}，耗时：{round(_t - _s, 2)} ")


#创建新线程
# da_list = [158, 216, 215, 197, 137, 194, 144, 154, 164, 219, 216, 189]
da_list = [158, 216, 215, 197, 137, 194, 144, 154, 164, 219, 189]
# da_list = [113, 217, 157, 188, 226, 149, 211, 223, 153]
threads = [ConfigProcess(da_list[i], f"10.0.5.{da_list[i]}") for i in range(len(da_list))]
# thread_1 = ConfigThread(1, "Thread-1")
# thread_2 = ConfigThread(2, "Thread-2")

#开启线程
if __name__ == '__main__':
    _start = time.time()
    for p in threads:
        time.sleep(2)
        # p.daemon = True
        p.start()
        # p.join()  # 等待p停止,等0.0001秒就不再等了
    _end = time.time()
    print(f'done total time is: {_end - _start} seconds')