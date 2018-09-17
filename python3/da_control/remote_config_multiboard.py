from DAboard import *
from get_board_ip import get_ip_list
from DAboard import *
import filecmp
import os

# 获取带配置文件的信息， 文件长度， 配置类型， FLASH配置地址
block_size = 65536
def get_config_info(source_file_name):
    filesize = os.path.getsize(source_file_name)
    print('待配置文件大小:{0}'.format(filesize))
    file = open(source_file_name,'rb')
    source_data = file.read(filesize)
    file.close()
    head_bytes = source_data[88:92]
    # print(h)
    # head_bytes = h
    flash_addr_pos = 104
    file_flash_type = 'SPANSION'
    if(head_bytes == b'\x30\x03\xe0\x01'):
        file_flash_type = 'MICRON'
        flash_addr_pos = 124
    # print(source_data[flash_addr_pos:flash_addr_pos+4])
    # print(struct.unpack('>l',source_data[flash_addr_pos:flash_addr_pos+4]))
    fallbacken = source_data[flash_addr_pos+11]
    file_flash_nxt_addr = struct.unpack('>l',source_data[flash_addr_pos:flash_addr_pos+4])[0]
    # print(fallbacken, file_flash_nxt_addr)

    # print(source_data[-256:-1])

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
def get_flash_type_str(da):
    flash_type = da.GetFlashType()
    flash_type_str = '错误'
    if flash_type == da.board_def.MICRON_FLASH:
        flash_type_str = 'MICRON'
    elif flash_type == da.board_def.SPANSION_FLASH:
        flash_type_str = 'SPANSION'
    return flash_type_str

def wait_erease_flash(da):
    for i in range(15):
        time.sleep(4)
        prog_status = da.GetEraseStatus()
        print('等待{0}秒'.format(i*4))
        if(prog_status == 255):
            break

    print('Erase done')
def write_flash(da, source_data, start_addr, is_first_page):
    temp_src = source_data+source_data[-260:-1]
    if(is_first_page==1):#不是写入第一页数据时，多写一点数据到目的端，确保有效配置数据全部写入flash
        temp_src = source_data
        # print(temp_src)
    da.WriteFLASH(temp_src, start_addr, is_first_page)
    # TODO 这条命令发出后可以读取状态包917字节（从0开始）， 为1表示错误发生，应停止后续操作，等待重配置生效后再进行
    del temp_src
def read_flash(da, flash_addr, target_file_name, filesize):
    target_file = open(target_file_name,'ab')
    print('read back config data start')
    data1 = da.Read_RAM(flash_addr, filesize)
    print('read back config data end')
    target_file.write(data1)
    target_file.close()

def get_das(board_list):
    das = []
    ip_list = get_ip_list(board_list)
    for ip in ip_list:
        da = DABoard()
        board_status = da.connect(ip)
        if(board_status != 1):
            ip_list.delete(ip)
            print('连接失败，请检查{0}'.format(ip))
        else:
            das.append(da)
    return das, ip_list
def da_config_flash(board_list, source_file_name1, source_file_name2):
    das, ips = get_das(board_list)
    config_infos = []

    file_flash_type1,flash_addr1, filesize1, update_file1, golden_file1, source_data1 = get_config_info(source_file_name1)
    file_flash_type2,flash_addr2, filesize2, update_file2, golden_file2, source_data2 = get_config_info(source_file_name2)
    source_data = [source_data1, source_data2]
    pages = (max(filesize1, filesize2) >> 8)+1
    for idx, da in enumerate(das):
        ip = ips[idx]
        flash_type_str = get_flash_type_str(da)

        if flash_type_str == file_flash_type1:
            target_file_name = source_file_name1.replace('.bin', '-'.join(['',ip,'rd_back.bin']))
            config_infos.append([target_file_name, file_flash_type1,flash_addr1, filesize1, 0])
        elif flash_type_str ==  file_flash_type2:
            target_file_name = source_file_name2.replace('.bin', '-'.join(['',ip,'rd_back.bin']))
            config_infos.append([target_file_name, file_flash_type2,flash_addr2, filesize2, 1])
        else:
            print('配置信息错误：板上FLASH类型：{0:s}；文件 FLASH类型：{1:s}'.format(flash_type_str, file_flash_type1))
            das.remove(da)
            ips.remove(ip)
        print('配置信息：写入地址：{0:x}；FLASH类型：{1:s}'.format(flash_addr1, flash_type_str))

    start_time = time.time()
    reprog_time = 35000
    reset_time = 30000

    # print(golden_file,flash_addr, flash_type_str )
    for idx, da in enumerate(das):
        target_file_name, file_flash_type,flash_addr, filesize, source_data_idx = config_infos[idx]
        print('可靠配置，首先设置看门狗计数，禁止喂狗，重配置超时时间：{0}，重复位超时时间：{1}'.format(reprog_time, reset_time))
        da.Set_watchdog_timeout(reprog_timeout=reprog_time, reset_timeout=reset_time)
        print(' 写入前面256字节数据到软核数据缓冲区')
        write_flash(da, source_data[source_data_idx][0:256], flash_addr, 1)

    for da in das:
        target_file_name, file_flash_type,flash_addr, filesize, source_data_idx = config_infos[idx]
        print('根据FLASH特性，先擦除除第一个block外的所有block，最后再擦除第一个block')
        print('擦除其他block')
        da.EraseFlashSector(flash_addr+block_size, (int)(filesize/block_size))

    for da in das:
        wait_erease_flash(da)

    for da in das:
        target_file_name, file_flash_type,flash_addr, filesize, source_data_idx = config_infos[idx]
        print('擦除第一个block, 该条命令，因为只擦1个block，自动将第一页数据写入FLASH')
        da.EraseFlashSector(flash_addr, 1)
    time.sleep(1) ##留时间擦除

    #第一页已经写入FLASH
    for page_idx in range(1,pages):
        for da in das:
            target_file_name, file_flash_type,flash_addr, filesize, source_data_idx = config_infos[idx]
            print('配置剩余所有数据')
            write_flash(da, source_data[(page_idx<<8):(page_idx+1)<<8], flash_addr+(page_idx<<8), 1)
            # read_flash(da, flash_addr, target_file_name, filesize)
    #读取数据
    for da in das:
        target_file_name, file_flash_type,flash_addr, filesize, source_data_idx = config_infos[idx]
        target_file = open(target_file_name,'wb')
        target_file.close()

    for page_idx in range((pages>>4)+1):
        for da in das:
            target_file_name, file_flash_type,flash_addr, filesize, source_data_idx = config_infos[idx]
            read_flash(da, flash_addr+(page_idx<<10), target_file_name, 1024)

    ######################
    end_time = time.time()
    # print(len(data1))
    print('time is{}'.format(end_time-start_time))
    for da in das:
        da.DA_reset()
        da.disconnect()

    if filecmp.cmp(source_file_name, target_file_name):
        return True
    else:
        return False

if __name__ == '__main__':
    condigs1 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_62_25_SPANSION_U.bin'
    condigs2 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_62_25_MICRON_U.bin'
    da_board_list1 = ['F02', 'F05']
    if da_config_flash(da_board_list1, condigs1, condigs2):
        sucess += 1
        print('configure successfull')
    else:
        failure += 1
        print('Error: confugure failed')
    print('成功{0}次，失败{1}次'.format(sucess, failure))
