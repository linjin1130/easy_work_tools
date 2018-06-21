from DAboard import *
import time
import matplotlib.pyplot as plt
da2 = DABoard()
da2_ip = '10.0.5.3'
board_status2 = da2.connect(da2_ip)
da2.setDAADSyncDelay(250)
da2.disconnect()