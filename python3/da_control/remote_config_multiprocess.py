from remote_config import *

u_file = 'B:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_73_32_SPANSION_U.bin'
g_file = 'B:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_73_32_SPANSION_G.bin'

da_list = [158, 216, 215, 197,194, 137, 144, 219, 214, 189, 210, 193]
da_list += [158, 216, 215, 197, 137, 194, 144, 154, 164, 219, 189]
da_list += [113, 217, 157, 188, 226, 149, 211, 223, 153]
da_list += [157, 217, 188, 149, 211, 223, 153, 226, 164, 154]
da_list = [4, 16, 28, 113, 137, 156, 157, 158, 164, 188, 193, 197, 200, 208, 213, 214, 219, 223, 226]
da_list = [2]
serial = 5

from multiprocessing import Pool
import os, time, random

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    da_list = set(da_list)
    p = Pool((len(da_list)))
    for id in da_list:
        time.sleep(0.1)
        p.apply_async(flash_config, args=(f'10.0.{serial}.{id}',id, g_file, u_file, ))
    # print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')