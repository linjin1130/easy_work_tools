from DAboard import *
import filecmp

import matplotlib.pyplot as plt
da = DABoard()
new_ip = '10.0.2.5'

board_status = da.connect(new_ip)
# da.Run_Command(26,0,0)
# da.Init()
# da.InitBoard()
da.SetIsMaster(1)
# da.ClearTrigCount()
da.disconnect()
if board_status < 0:
    print('Failed to find board')