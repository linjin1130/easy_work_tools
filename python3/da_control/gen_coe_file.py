import struct
target_file = open('ram.coe','w')
target_file.write('MEMORY_INITIALIZATION_RADIX=16;\n')
target_file.write('MEMORY_INITIALIZATION_VECTOR=\n')
data_list = [i%65536 for i in range(3500*32)]
print(len(data_list))
data_list = [(i<<11)-1 for i in range(1,33)]*3500
print(len(data_list), data_list[0:32])
fmt = '>{0}H'.format(32)
n=[]
for i in range(3500):
    n.append(struct.pack(fmt, *(data_list[i*32:(i+1)*32])).hex())

str_list = ','.join(n)
target_file.write(str_list)
target_file.write(';')