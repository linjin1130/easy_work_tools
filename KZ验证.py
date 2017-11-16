import sys, os
import struct
onpath = os.getcwd()
##uopath = unicode(onpath , "utf8")
print onpath
data = range(1,257)
##print data
#outfilename = unicode(opathname , "utf8")
kz_verify_rnd = os.path.join(onpath,"kz_verify_rnd.dat")
output_file_verify = open(kz_verify_rnd, 'wb')
kz_verify_rnd = os.path.join(onpath,"kz_raw_rnd.dat")
output_file_raw = open(kz_verify_rnd, 'wb')
##data = input_file.read(2048)##读取前8个字节
lz_primary_slave = 0x0A
for num in data:
    num = num%256
    print ("原始随机数:%x\t"%(num))
    output_file_raw.write(struct.pack('B', num))
    ch = num & 0x0F
    if( (ch & 0xC) == 0):
        verify_data = 0;
    if( ch == 1):
        verify_data = 1 << ((lz_primary_slave & 0x01) << 3);
    if( ch == 5):
        verify_data = 2 << ((lz_primary_slave & 0x02) << 2);
    if( ch == 9):
        verify_data = 4 << ((lz_primary_slave & 0x04) << 1);
    if( ch == 13):
        verify_data = 8 << ((lz_primary_slave & 0x08) << 0);
    if( ch == 2 | ch == 3):
        verify_data = 0x0010  << ((lz_primary_slave & 0x01) << 3);
    if( ch == 6 | ch == 7):
        verify_data = 0x0020  << ((lz_primary_slave & 0x02) << 2);
    if( ch == 10 | ch == 11):
        verify_data = 0x0040  << ((lz_primary_slave & 0x04) << 1);
    if( ch == 14 | ch == 15):
        verify_data = 0x0080  << ((lz_primary_slave & 0x08) << 0);
    print ("低半字节：%x\t"%(verify_data))
    output_file_verify.write(struct.pack('H', verify_data))
    ch = (num >> 4) & 0x0F
    if( (ch & 0xC) == 0):
        verify_data = 0;
    if( ch == 1):
        verify_data = 1 << ((lz_primary_slave & 0x01) << 3);
    if( ch == 5):
        verify_data = 2 << ((lz_primary_slave & 0x02) << 2);
    if( ch == 9):
        verify_data = 4 << ((lz_primary_slave & 0x04) << 1);
    if( ch == 13):
        verify_data = 8 << ((lz_primary_slave & 0x08) << 0);
    if( ch == 2 | ch == 3):
        verify_data = 0x0010  << ((lz_primary_slave & 0x01) << 3);
    if( ch == 6 | ch == 7):
        verify_data = 0x0020  << ((lz_primary_slave & 0x02) << 2);
    if( ch == 10 | ch == 11):
        verify_data = 0x0040  << ((lz_primary_slave & 0x04) << 1);
    if( ch == 14 | ch == 15):
        verify_data = 0x0080  << ((lz_primary_slave & 0x08) << 0);
    print ("高半字节：%x"%(verify_data))
    output_file_verify.write(struct.pack('H', verify_data))
##    switch (ch)
##    {
##        case 0: verify_data = 0;
##        case 4: verify_data = 0;
##        case 8: verify_data = 0;
##        case C: verify_data = 0;
##        case 1: verify_data = 1 << ((lz_primary_slave & 0x01) << 3);
##        case 5: verify_data = 2 << ((lz_primary_slave & 0x02) << 2);
##        case 9: verify_data = 4 << ((lz_primary_slave & 0x04) << 1);
##        case 13: verify_data = 8 << ((lz_primary_slave & 0x08) << 0);
##        case 2: verify_data = 0x0010  << ((lz_primary_slave & 0x01) << 3);
##        case 3: verify_data = 0x0010  << ((lz_primary_slave & 0x01) << 3);
##        case 6: verify_data = 0x0020  << ((lz_primary_slave & 0x02) << 2);
##        case 7: verify_data = 0x0020  << ((lz_primary_slave & 0x02) << 2);
##        case 10: verify_data = 0x0040 << ((lz_primary_slave & 0x04) << 1);
##        case 11: verify_data = 0x0040 << ((lz_primary_slave & 0x04) << 1);
##        case 14: verify_data = 0x0080 << ((lz_primary_slave & 0x08) << 0);
##        case 15: verify_data = 0x0080 << ((lz_primary_slave & 0x08) << 0);
##    }
    
    
##print 'close finally'
output_file_verify.close()
output_file_raw.close()
