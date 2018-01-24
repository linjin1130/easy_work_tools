#1. 执行命令读取ARP信息
#2. 在信息中取得内网对应的MAC口编号
#3. 根据编号进入到ARP和DA boards key的生成

#import os
import subprocess

cmd = 'cmd.exe /c F:\\PycharmProjects\\easy_work_tools\\python3\\DA_Key\\arp_info.bat'

p = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)

curline = p.stdout.readline()

while(curline != b''):
    str_info = str(curline,encoding="gbk")
    # print(str_info)
    if str_info.find('10.0.') > 0:
        # print(str_info)
        MAC_num = str_info.split('0x')[1]
        print(MAC_num)
        break
    curline = p.stdout.readline()  
      
p.wait()  
print(p.returncode) 