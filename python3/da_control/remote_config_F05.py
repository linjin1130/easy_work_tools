from remote_config import *

condigs1 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\\DA_AD_PRJ_V21\CONFIG_FILES\\V01_22_6_SPANSION_U.bin'
condigs2 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\\DA_AD_PRJ\CONFIG_FILES\\V01_71_28_MICRON_U.bin'
new_ip = '10.0.5.5'
if int(new_ip.split('.')[2]) > 4:
    source_file_name = condigs1
else:
    source_file_name = condigs2

sucess = 0
failure = 0
for i in range(1):
    if da_config_flash(new_ip, source_file_name,erase=True, is_old_version=False):
        sucess += 1
        print('configure successfull')
    else:
        failure += 1
        print('Error: confugure failed')
    print('成功{0}次，失败{1}次'.format(sucess, failure))
