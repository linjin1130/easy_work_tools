from DAboard import *
from DAboard_defines import *
import filecmp
import os

# 获取带配置文件的信息， 文件长度， 配置类型， FLASH配置地址
def get_config_info(source_file_name):
    filesize = os.path.getsize(source_file_name)
    print('待配置文件大小:{0}'.format(filesize))
    file = open(source_file_name,'rb')
    source_data = file.read(filesize)
    head_bytes = source_data[88:92]
    # print(h)
    # head_bytes = h
    flash_addr_pos = 104
    file_flash_type = DABoard_Defines.SPANSION_FLASH
    if(head_bytes == b'\x30\x03\xe0\x01'):
        file_flash_type = DABoard_Defines.MICRON_FLASH
        flash_addr_pos = 124
    # print(source_data[flash_addr_pos:flash_addr_pos+4])
    # print(struct.unpack('>l',source_data[flash_addr_pos:flash_addr_pos+4]))
    fallbacken = source_data[flash_addr_pos+11]
    file_flash_nxt_addr = struct.unpack('>l',source_data[flash_addr_pos:flash_addr_pos+4])[0]
    print(fallbacken, file_flash_nxt_addr)

    print(source_data[-256:-1])

    golden_file = 0
    flash_addr = 0x00F50000
    if file_flash_nxt_addr == 0x00F50000 and fallbacken == 15:
        golden_file = 1
        flash_addr = 0
        print('warning golden file')

    update_file = 0
    if file_flash_nxt_addr == 0 and fallbacken == 0:
        update_file = 1

    return file_flash_type, flash_addr, filesize, update_file, golden_file, source_data

#参数检查， 返回配置FLASH类型和类型是否合法
def config_para_check(da, file_flash_type, update_file, golden_file):
    flash_type = da.GetFlashType()

    config_info_valid = 0
    # print(flash_type )
    # if flash_type == da.board_def.MICRON_FLASH and source_file_name.find('_M_'):
    if flash_type == file_flash_type:
        config_info_valid = 1
        print('flash type correct')

    config_info_valid += update_file + golden_file
    if flash_type == da.board_def.MICRON_FLASH:
        flash_type_str = 'MICRON'
    elif flash_type == da.board_def.SPANSION_FLASH:
        flash_type_str = 'SPANSION'
    else:
        flash_type_str = '错误'
    return config_info_valid, flash_type_str

def erease_flash(da,flash_addr, filesize):
    da.EraseFlashSector(flash_addr, (int)(filesize/65536) +2)
    for i in range(60):
        prog_status = da.GetEraseStatus()
        print(prog_status,i)
        if(prog_status == 255):
            break
        time.sleep(10)
    print('Erase done')
def write_flash(da, golden_file, source_data):
    temp_src = source_data+source_data[-260:-1]
    if golden_file == 1:
        da.WriteGoldenFLASH(temp_src)
    else:
        da.WriteFLASH(temp_src)
    del temp_src
def read_flash(da, flash_addr, target_file_name, filesize):
    target_file = open(target_file_name,'wb')
    print('read back config data start')
    data1 = da.Read_RAM(flash_addr, filesize)
    print('read back config data end')
    target_file.write(data1)
    target_file.close()

def da_config_flash(new_ip, source_file_name):
    da = DABoard()
    board_status = da.connect(new_ip)
    target_file_name = source_file_name.replace('.bin', '-'.join(['',new_ip,'rd_back.bin']))
    file_flash_type,flash_addr, filesize, update_file, golden_file, source_data = get_config_info(source_file_name)
    config_info_valid, flash_type_str = config_para_check(da, file_flash_type, update_file, golden_file)
    if config_info_valid == 0:
        print('配置参数有误，请检查')
        return False
    print('配置信息：写入地址：{0:x}；FLASH类型：{1:s}'.format(flash_addr, flash_type_str))
    start_time = time.time()
    erease_flash(da,flash_addr, filesize)
    write_flash(da, golden_file, source_data)
    read_flash(da, flash_addr, target_file_name, filesize)
    end_time = time.time()
    # print(len(data1))
    print('time is{}'.format(end_time-start_time))

    if filecmp.cmp(source_file_name, target_file_name):
        # da.DA_reset()
        da.disconnect()
        return True
    else:
        da.disconnect()
        return False

if __name__ == '__main__':
    condigs1 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_43_10_SPANSION_U.bin'
    condigs2 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_44_10_MICRON_U.bin'
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
