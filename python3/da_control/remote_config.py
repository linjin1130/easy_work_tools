import time

from DAboard import *
from DAboard_defines import *
import filecmp
import os

# 获取带配置文件的信息， 文件长度， 配置类型， FLASH配置地址
block_size = 65536
def get_config_info(source_file_name):
    filesize = os.path.getsize(source_file_name)
    # print('待配置文件大小:{0}'.format(filesize))
    file = open(source_file_name,'rb')
    source_data = file.read(filesize)
    file.close()
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
    # print(fallbacken, file_flash_nxt_addr)

    # print(source_data[-256:-1])

    golden_file = 0
    flash_addr = 0x00F50000
    if file_flash_nxt_addr == 0x00F50000 and fallbacken == 15:
        golden_file = 1
        flash_addr = 0
        # print('warning golden file')

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
    flash_type_str = '错误'
    if flash_type == file_flash_type:
        config_info_valid = 1
    else:
        print(f'warnning {da.ip} flash type is not correct')
        return config_info_valid, flash_type_str

    config_info_valid += update_file + golden_file
    if flash_type == da.board_def.MICRON_FLASH:
        flash_type_str = 'MICRON'
    elif flash_type == da.board_def.SPANSION_FLASH:
        flash_type_str = 'SPANSION'
    else:
        flash_type_str = '错误'
    return config_info_valid, flash_type_str

def erease_flash(da,flash_addr, filesize):
    da.EraseFlashSector(flash_addr, (int)(filesize/block_size))
    for i in range(150):
        time.sleep(0.4)
        prog_status = da.GetEraseStatus()
        if(prog_status == 255):
            break
        if i > 140:
            print('擦除失败')
            # print('等待{0}秒'.format(i * 4 + 4))

    # print(f'{da.ip} Erase done')
def write_flash(da, source_data, start_addr, is_first_page):
    temp_src = source_data+source_data[-260:-1]
    if(is_first_page==1):#不是写入第一页数据时，多写一点数据到目的端，确保有效配置数据全部写入flash
        temp_src = source_data
        # print(temp_src)
    da.WriteFLASH(temp_src, start_addr, is_first_page)
    # TODO 这条命令发出后可以读取状态包917字节（从0开始）， 为1表示错误发生，应停止后续操作，等待重配置生效后再进行
    del temp_src
def read_flash(da, flash_addr, target_file_name, filesize):
    target_file = open(target_file_name,'wb')
    # print(f'{da.ip} read back config data start')
    data1 = da.Read_RAM(flash_addr, filesize)
    # print(f'{da.ip} read back config data end')
    target_file.write(data1)
    target_file.close()

def da_erase_flash(new_ip, source_file_name, erase=True, is_old_version=False):
    da = DABoard()
    board_status = da.connect(new_ip, print_msg = False)
    if(board_status != 1):
        print(f'{new_ip} 连接失败，请检查')
        return False

    target_file_name = source_file_name.replace('.bin', '-'.join(['',new_ip,'rd_back.bin']))
    file_flash_type,flash_addr, filesize, update_file, golden_file, source_data = get_config_info(source_file_name)

    config_info_valid, flash_type_str = config_para_check(da, file_flash_type, update_file, golden_file)
    if config_info_valid == 0:
        print(f'{new_ip} 配置参数有误，请检查')
        return False
    # print('配置信息：写入地址：{0:x}；FLASH类型：{1:s}'.format(flash_addr, flash_type_str))
    start_time = time.time()
    reprog_time = 65000
    reset_time = 60000

    # print(golden_file,flash_addr, flash_type_str )
    if(golden_file == 1 and flash_addr == 0 and flash_type_str == 'SPANSION'):
        reprog_time = 65500
        reset_time = 65000
        # print('可靠配置，首先设置看门狗计数，禁止喂狗，重配置超时时间：{0}秒，重复位超时时间：{1}秒'.format(reprog_time/100.0, reset_time/100.0))
        da.Set_watchdog_timeout(reprog_timeout=reprog_time, reset_timeout=reset_time)

        if erase:
            # print('SPANSION FLASH 第一个block用块擦除的方式无法擦除，临时的办法是整个FLASH擦除')
            sta = da.EraseFlashEntire()
            # sta = da.disconnect(new_ip)
    else:
        return False
    ######################
    print(f'{new_ip} erasing, wait 100 second')
    for i in range(100):
        time.sleep(1)
    for i in range(1000):
        time.sleep(0.1)
        if (i % 100) == 0:
            # print(f'{new_ip} 已等待{i/10}秒：重连设备')
            da.disconnect(print_msg = False)
            da = DABoard()
            if da.connect(new_ip, print_msg = False):
                # print(f'{new_ip} 擦除成功')
                end_time = time.time()
                # print(len(data1))
                print(f'{new_ip} 擦除成功 erase time is {round(end_time - start_time, 2)}')
                return True

    end_time = time.time()
    # print(len(data1))
    # print(f'{new_ip} erase time is{end_time - start_time}')
    return False

def da_config_flash(new_ip, source_file_name, erase=False, is_old_version=False):
    da = DABoard()
    board_status = da.connect(new_ip, print_msg = False)
    if(board_status != 1):
        print(f'{new_ip} 连接失败，请检查')
        return False
    target_file_name = source_file_name.replace('.bin', '-'.join(['',new_ip,'rd_back.bin']))
    file_flash_type,flash_addr, filesize, update_file, golden_file, source_data = get_config_info(source_file_name)

    config_info_valid, flash_type_str = config_para_check(da, file_flash_type, update_file, golden_file)
    if config_info_valid == 0:
        print(f'{new_ip} 配置参数有误，请检查')
        return False
    # print('配置信息：写入地址：{0:x}；FLASH类型：{1:s}'.format(flash_addr, flash_type_str))
    start_time = time.time()
    reprog_time = 65000
    reset_time = 60000

    # print(golden_file,flash_addr, flash_type_str )
    if(golden_file == 1 and flash_addr == 0 and flash_type_str == 'SPANSION'):
        reprog_time = 65500
        reset_time = 65000
        # print('可靠配置，首先设置看门狗计数，禁止喂狗，重配置超时时间：{0}秒，重复位超时时间：{1}秒'.format(reprog_time/100.0, reset_time/100.0))
        da.Set_watchdog_timeout(reprog_timeout=reprog_time, reset_timeout=reset_time)

        if erase:
            # print('SPANSION FLASH 第一个block用块擦除的方式无法擦除，临时的办法是整个FLASH擦除')
            da.EraseFlashEntire()
        # else:
        #     print('这是一块新FLASH，不用擦除')
        write_flash(da, source_data, flash_addr, 0)
    elif is_old_version:
        # print('可靠配置，首先设置看门狗计数，禁止喂狗，重配置超时时间：{0}，重复位超时时间：{1}'.format(reprog_time, reset_time))
        da.Set_watchdog_timeout(reprog_timeout=reprog_time, reset_timeout=reset_time)
        if erase:
            # print('擦除')
            erease_flash(da, flash_addr + block_size, filesize + block_size)
        # print('老版本远程配置，配置所有数据')
        if flash_addr == 0:
            da.WriteGoldenFLASH_old(source_data+source_data[-256:])
        else:
            da.WriteFLASH_old(source_data+source_data[-256:])
    else:
        # print('可靠配置，首先设置看门狗计数，禁止喂狗，重配置超时时间：{0}，重复位超时时间：{1}'.format(reprog_time, reset_time))
        da.Set_watchdog_timeout(reprog_timeout=reprog_time, reset_timeout=reset_time)
        # print(' 写入前面256字节数据到软核数据缓冲区')
        write_flash(da, source_data[0:256], flash_addr, 1)
        # print('根据FLASH特性，先擦除除第一个block外的所有block，最后再擦除第一个block')
        if erase:
            # print('擦除其他block')
            erease_flash(da,flash_addr+block_size, filesize+block_size)
        # print('新版本配置，擦除第一个block, 该条命令，因为只擦1个block，自动将第一页数据写入FLASH')
        erease_flash(da,flash_addr, block_size)
        # print('配置剩余所有数据')
        write_flash(da, source_data[256:], flash_addr+256, 0)
    read_flash(da, flash_addr, target_file_name, filesize)


    ######################
    end_time = time.time()
    # print(len(data1))
    # print(f'{new_ip} config time is{end_time-start_time}')

    stat = True
    if filecmp.cmp(source_file_name, target_file_name):
        if golden_file == 0:
            da.DA_reprog()
        da.disconnect( print_msg = False)
        stat = True
    else:
        da.disconnect( print_msg = False)
        stat = False

    note = '失败'
    if stat:
        note = '成功'
    f_name = '配置记录.txt'
    if not os.path.exists(f_name):
        with open(f_name, 'w') as f:
            pass

    with open(f_name, 'a') as f:
        f.write(','.join([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),new_ip, note, source_file_name, '\n']))
    return stat

def da_config_flash(new_ip, source_file_name, erase=False, is_old_version=False):
    da = DABoard()
    board_status = da.connect(new_ip, print_msg = False)
    if(board_status != 1):
        print(f'{new_ip} 连接失败，请检查')
        return False
    target_file_name = source_file_name.replace('.bin', '-'.join(['',new_ip,'rd_back.bin']))
    file_flash_type,flash_addr, filesize, update_file, golden_file, source_data = get_config_info(source_file_name)

    config_info_valid, flash_type_str = config_para_check(da, file_flash_type, update_file, golden_file)
    if config_info_valid == 0:
        print(f'{new_ip} 配置参数有误，请检查')
        return False
    # print('配置信息：写入地址：{0:x}；FLASH类型：{1:s}'.format(flash_addr, flash_type_str))
    start_time = time.time()
    reprog_time = 65000
    reset_time = 60000

    # print(golden_file,flash_addr, flash_type_str )
    if(golden_file == 1 and flash_addr == 0 and flash_type_str == 'SPANSION'):
        reprog_time = 65500
        reset_time = 65000
        # print('可靠配置，首先设置看门狗计数，禁止喂狗，重配置超时时间：{0}秒，重复位超时时间：{1}秒'.format(reprog_time/100.0, reset_time/100.0))
        da.Set_watchdog_timeout(reprog_timeout=reprog_time, reset_timeout=reset_time)

        if erase:
            # print('SPANSION FLASH 第一个block用块擦除的方式无法擦除，临时的办法是整个FLASH擦除')
            da.EraseFlashEntire()
        # else:
        #     print('这是一块新FLASH，不用擦除')
        write_flash(da, source_data, flash_addr, 0)
    elif is_old_version:
        # print('可靠配置，首先设置看门狗计数，禁止喂狗，重配置超时时间：{0}，重复位超时时间：{1}'.format(reprog_time, reset_time))
        da.Set_watchdog_timeout(reprog_timeout=reprog_time, reset_timeout=reset_time)
        if erase:
            # print('擦除')
            erease_flash(da, flash_addr + block_size, filesize + block_size)
        # print('老版本远程配置，配置所有数据')
        if flash_addr == 0:
            da.WriteGoldenFLASH_old(source_data+source_data[-256:])
        else:
            da.WriteFLASH_old(source_data+source_data[-256:])
    else:
        # print('可靠配置，首先设置看门狗计数，禁止喂狗，重配置超时时间：{0}，重复位超时时间：{1}'.format(reprog_time, reset_time))
        da.Set_watchdog_timeout(reprog_timeout=reprog_time, reset_timeout=reset_time)
        # print(' 写入前面256字节数据到软核数据缓冲区')
        write_flash(da, source_data[0:256], flash_addr, 1)
        # print('根据FLASH特性，先擦除除第一个block外的所有block，最后再擦除第一个block')
        if erase:
            # print('擦除其他block')
            erease_flash(da,flash_addr+block_size, filesize+block_size)
        # print('新版本配置，擦除第一个block, 该条命令，因为只擦1个block，自动将第一页数据写入FLASH')
        erease_flash(da,flash_addr, block_size)
        # print('配置剩余所有数据')
        write_flash(da, source_data[256:], flash_addr+256, 0)
    read_flash(da, flash_addr, target_file_name, filesize)


    ######################
    end_time = time.time()
    # print(len(data1))
    # print(f'{new_ip} config time is{end_time-start_time}')

    stat = True
    if filecmp.cmp(source_file_name, target_file_name):
        if golden_file == 0:
            da.DA_reprog()
        da.disconnect( print_msg = False)
        stat = True
    else:
        da.disconnect( print_msg = False)
        stat = False

    note = '失败'
    if stat:
        note = '成功'
    f_name = '配置记录.txt'
    if not os.path.exists(f_name):
        with open(f_name, 'w') as f:
            pass

    with open(f_name, 'a') as f:
        f.write(','.join([time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),new_ip, note, source_file_name, '\n']))
    return stat

def version_check(ip):
    da = DABoard()
    board_status = da.connect(ip, print_msg = False)
    if (board_status != 1):
        print(f'{ip} 连接失败，请检查')
        return False
    ver = da.GetVersion()
    # print(ver)
    return ver[2] >= 73

def config_run(ip, g_file, u_file):
    # V01_69_28_SPANSION_U_SLH_LW
    new_ip = ip
    source_file_name = g_file
    sucess = 0
    failure = 0

    if version_check(new_ip):
        ## 软件版本> 73时

        if da_erase_flash(new_ip, source_file_name) is not True:
            print(f'{ip} 擦除失败， 请检查')
            return
        print(f'{ip} 写golden区域,约100-300秒')
        if da_config_flash(new_ip, source_file_name, erase=False):
            sucess += 1
            # print(f'{ip} configure successfull')
        else:
            failure += 1
            # print(f'{ip} Error: confugure failed')
        print(f'{ip} 成功{sucess}次，失败{failure}次')
    else:
        print(f'{ip} 写golden区域,约100-300秒')
        if da_config_flash(new_ip, source_file_name, erase=True):
            sucess += 1
            # print('configure successfull')
        else:
            failure += 1
            # print('Error: confugure failed')
        print(f'{ip} 成功{sucess}次，失败{failure}次')

    source_file_name = u_file
    print(f'{ip} 写update区域,约100-300秒')
    if da_config_flash(new_ip, source_file_name, erase=False):
        sucess += 1
        # print('configure successfull')
    else:
        failure += 1
        # print('Error: confugure failed')
    print(f'{ip} 成功{sucess}次，失败{failure}次')

def flash_config(ip, name, g_file, u_file):
    # print('id %s, Run task %s (%s)...' % (name, ip, os.getpid()))
    start = time.time()
    time.sleep(1)
    config_run(ip, g_file, u_file)
    # time.sleep(random.random() * 3)
    end = time.time()
    msg = 'Task %s runs %0.2f seconds.' % (name, (end - start))
    print(msg)
# if __name__ == '__main__':
#     condigs1 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_46_11_SPANSION_U.bin'
#     condigs2 = 'D:\\FPGA\\vivado_2016_4\\AD_DA\\DA_AD_PRJ\\CONFIG_FILES\\V01_44_10_MICRON_U.bin'
#     new_ip = '10.0.5.7'
#     if int(new_ip.split('.')[2]) > 4:
#         source_file_name = condigs1
#     else:
#         source_file_name = condigs2
#
#     sucess = 0
#     failure = 0
#     for i in range(1):
#         if da_config_flash(new_ip, source_file_name):
#             sucess += 1
#             print('configure successfull')
#         else:
#             failure += 1
#             print('Error: confugure failed')
#         print('成功{0}次，失败{1}次'.format(sucess, failure))
