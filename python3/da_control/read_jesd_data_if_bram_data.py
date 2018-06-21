from DAboard import *
import filecmp

import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.2.5'

board_status = da.connect(new_ip)
cnt = 0
da.SetRamRead(1)
tmp = b''
target_file = open('bram_data','wb')
start_time = time.time()
for i in range(1000000):

    tmp = da.Read_RAM(0,1000000)
    del tmp
    # time.sleep(3)
    # target_file.write(tmp)
    cnt+=1
    print(cnt)

end_time = time.time()
# print(len(data1))
print('time is{}'.format(end_time-start_time))
target_file.close()

da.disconnect()
if board_status < 0:
    print('Failed to find board')