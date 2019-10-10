import pi_control as pi_core
from data_aquire_control import *
from DAboard import *
import matplotlib.pyplot as plt

# experiment parameter
start_pos = [0, 0]
end_pos = [101, 101]
step_size = [1, 1]
TABLERATE = 10 # T = x * 50us  20 is 1ms
sample_period = 50e-6

# instance pi
pi_ip = '172.16.0.35'
daq_ip = '172.16.0.170'


pi_core.TABLERATE = TABLERATE
pidevice = pi_core.get_pidev(pi_ip)

pi_core.pidev_genwave(pidevice, start_pos=start_pos, end_pos=end_pos, step_size=step_size)
pi_core.pidev_prepare(pidevice, start_pos=start_pos)


daq = DABoard()
board_status = daq.connect(daq_ip)
trig_cnt, data_shape = DataAquire_prepare(daq, start_pos=start_pos, end_pos=end_pos, step_size=step_size, TABLERATE=10, sample_period=sample_period)
print(trig_cnt, data_shape)
pi_core.pidev_run(pidevice, start_pos)
ret = DataAquire_start(daq, trig_cnt, data_shape, false_data=False)

time.sleep(1)
update_dataaquire_reg(daq)
print(len(ret))
# print(ret[0])
# print(ret[1])
hdf5_write('FPGA control board', ret)
daq.disconnect()

pos1 = ret[6]
pos2 = ret[7]
plt.figure()
plt.title('axis 1 and  axis 2 postion figure, up is axis 1, down is axis 2')
plt.subplot(211)
plt.plot(pos1[1])
plt.ylabel('mm')
plt.subplot(212)
plt.plot(pos2[1])
plt.ylabel('mm')
plt.xlabel(f'{sample_period*1e6}us/sample point')
plt.show()