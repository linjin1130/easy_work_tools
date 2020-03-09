import time
import datetime
from DAboard import *
from data_waves import *

da_list = [ 158, 216, 215, 197, 137, 194, 144, 219, 216, 189]
da_list = [ 137]
# das = [DABoard(id=f'F{id}', ip=f'10.0.5.{id}', data_offset=[0,0,0,0], batch_mode=True) for id in da_list]
da = DABoard()
new_ip = '10.0.5.149'
board_status = da.connect(addr=new_ip)
# da.DA_reset()
da.DA_reprog()
da.disconnect()
