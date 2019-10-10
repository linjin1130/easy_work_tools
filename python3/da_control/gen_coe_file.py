# 生成command表
import struct
target_file = open('seq.coe','w')
target_file.write('MEMORY_INITIALIZATION_RADIX=10;\n')
target_file.write('MEMORY_INITIALIZATION_VECTOR=\n')
unit = [(100000 >> 3) << 16, 0]
print(unit)
data_list1 = unit*4096
# data_list1.extend(data_list1)
# data_list1.extend(data_list1[0:56])
print(len(data_list1))
for idx in range(len(data_list1)):
    data_list1[idx] = str(data_list1[idx])

str_list = ','.join(data_list1)
target_file.write(str_list)
target_file.write(';')

# 生成command表
import numpy as np
target_file = open('wave.coe','w')
target_file.write('MEMORY_INITIALIZATION_RADIX=16;\n')
target_file.write('MEMORY_INITIALIZATION_VECTOR=\n')
unit = np.sin(np.arange(0, 2*np.pi, (2*np.pi)/200))*32767.5+32767.5
print(unit)
unit = unit.astype(np.uint32)
unit = list(unit)
print(unit)
new_u = []

def get_hex(data):
    _t = hex(data)[2:]
    if len(_t) == 1:
        _t = '000'+_t

    if len(_t) == 2:
        _t = '00'+_t


    if len(_t) == 3:
        _t = '0'+_t
    return _t

for idx in range(100):
    # print(idx)
    new_u.append(get_hex(unit[(idx << 1)+1 ]) + get_hex(unit[(idx << 1) + 0]))
print(new_u)
data_list1 = new_u * int(100000/200)

# data_list1.extend(data_list1)
# data_list1.extend(data_list1[0:56])
print(len(data_list1))
for idx in range(len(data_list1)-1):
    target_file.write(data_list1[idx]+',\n')
#     data_list1[idx] = str(data_list1[idx])
# str_list = ','.join(data_list1)
# print(data_list1)
# target_file.write(str_list)
target_file.write(data_list1[-1])
target_file.write(';')

# # 生成TDC对应的时间值查找表
# import struct
# target_file = open('tdc_lut.coe','w')
# target_file.write('MEMORY_INITIALIZATION_RADIX=10;\n')
# target_file.write('MEMORY_INITIALIZATION_VECTOR=\n')
# data_list1 = [i*40 for i in range(256)]
# # data_list1.extend(data_list1)
# # data_list1.extend(data_list1[0:56])
# # print(len(data_list1))
# for idx in range(len(data_list1)):
#     if data_list1[idx] >= 4000:
#         data_list1[idx] = str(4000)
#     else:
#         data_list1[idx] = str(data_list1[idx])
#
# str_list = ','.join(data_list1)
# target_file.write(str_list)
# target_file.write(';')

# 生成底层IODELAY对应0-4000ps之间的查找表
# import struct
# target_file = open('ram_div_4_iodelay.coe','w')
# target_file.write('MEMORY_INITIALIZATION_RADIX=10;\n')
# target_file.write('MEMORY_INITIALIZATION_VECTOR=\n')
# unit = round(1000/4.7)
# data_list1 = [str(round(i/4.7)) for i in range(1000)]
# data_list2 = [str((unit << 9) | int(i)) for i in data_list1]
# data_list3 = [str((unit << 18) | int(i)) for i in data_list2]
# data_list4 = [str((unit << 27) | int(i)) for i in data_list3]
#
# for item in data_list4:
#     print(hex(int(item)))
# # print(len(data_list))
# str_list = ','.join(data_list1+data_list2+data_list3+data_list4)
# target_file.write(str_list)
# target_file.write(';')

# 生成1000/5的查找表
# import struct
# target_file = open('ram_div_5.coe','w')
# target_file.write('MEMORY_INITIALIZATION_RADIX=10;\n')
# target_file.write('MEMORY_INITIALIZATION_VECTOR=\n')
# data_list = [str(round(i/5)) for i in range(1000)]
# print(len(data_list))
# str_list = ','.join(data_list)
# target_file.write(str_list)
# target_file.write(';')

# import struct
# target_file = open('ram.coe','w')
# target_file.write('MEMORY_INITIALIZATION_RADIX=16;\n')
# target_file.write('MEMORY_INITIALIZATION_VECTOR=\n')
# data_list = [i%65536 for i in range(3500*32)]
# print(len(data_list))
# data_list = [(i<<11)-1 for i in range(1,33)]*3500
# print(len(data_list), data_list[0:32])
# fmt = '>{0}H'.format(32)
# n=[]
# for i in range(3500):
#     n.append(struct.pack(fmt, *(data_list[i*32:(i+1)*32])).hex())
#
# str_list = ','.join(n)
# target_file.write(str_list)
# target_file.write(';')