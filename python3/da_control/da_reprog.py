from DAboard import *
da = DABoard()
new_ip = '10.0.5.5'
board_status = da.connect(new_ip)
# da.GetFlashType()
# da.DA_reset()
da.DA_reprog()
# da.InitBoard()
da.disconnect()