from remote_config import *

condigs1 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\awg_250M_192_S.bin'
condigs2 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_58_27_MICRON_U.bin'
new_ip = '10.0.5.140'
if int(new_ip.split('.')[2]) > 4:
    source_file_name = condigs1
else:
    source_file_name = condigs2

success = 0
failure = 0
for i in range(1):
    if da_config_flash(new_ip, source_file_name):
        success += 1
        print('configure successfull')
    else:
        failure += 1
        print('Error: confugure failed')
    print('成功{0}次，失败{1}次'.format(success, failure))
