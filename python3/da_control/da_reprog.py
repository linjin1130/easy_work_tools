from .DAboard import *
from .data_waves import *
da = DABoard()
new_ip = '10.0.4.8'
board_status = da.connect(new_ip)
# da.GetFlashType()
# da.DA_reset()
da.DA_reprog()
# da.InitBoard()
da.disconnect()