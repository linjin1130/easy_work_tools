from DAboard import *
import filecmp
import os

def da_config_flash(new_ip, source_file_name):
    da = DABoard()
    board_status = da.connect(new_ip)
    target_file_name = source_file_name.replace('.bin', 'rd_back.bin')
    filesize = os.path.getsize(source_file_name)
    print('待配置文件大小:{0}'.format(filesize))
    file = open(source_file_name,'rb')
    source_data = file.read(filesize)

    flash_addr = 0x00000000

    target_file = open(target_file_name,'wb')
    start_time = time.time()

    print('read back config data start')
    data1 = da.Read_RAM(flash_addr, filesize)
    print('read back config data end')
    # da.EraseFlashEntire()

    end_time = time.time()
    # print(len(data1))
    print('time is{}'.format(end_time-start_time))

    target_file.write(data1)
    target_file.close()

    if filecmp.cmp(source_file_name, target_file_name):
        # da.DA_reset()
        da.disconnect()
        return True
    else:
        da.disconnect()
        return False



# source_file_name = 'D:\\FPGA\\vivado_2016_3\\AD_DA\\DEL\\V0_0_M_G.bin'
# source_file_name = 'D:\\FPGA\\vivado_2016_3\\AD_DA\\DEL\\V0_0_S_G.bin'

condigs1 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_37_10_SPANSION_G.bin'
condigs2 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_37_10_MICRON_G.bin'
new_ip = '10.0.5.1'
if int(new_ip.split('.')[2]) > 4:
    source_file_name = condigs1
else:
    source_file_name = condigs2

sucess = 0
failure = 0
for i in range(1):
    if da_config_flash(new_ip, source_file_name):
        sucess += 1
        print('configure successfull')
    else:
        failure += 1
        print('Error: confugure failed')
    print('成功{0}次，失败{1}次'.format(sucess, failure))
