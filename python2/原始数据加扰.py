# -*- coding: utf-8 -*-
##struct Header
##{
##    char[4] tag1;
##    char[2] segseq;
##    char[2] segsize;
##}
##struct data
##{
##    char[2] tag_data;
##    char[1] dataseq;
##    char[0] tag;
##    char[60] real_data;
##}
import sys, os
import struct
inpath = 'C:/Program Files/TG02数据注入/coding/2K_原始数据-加扰.dat'
uipath = unicode(inpath , "utf8")
opath = 'C:/Program Files/TG02数据注入/coding/2K_原始数据-加扰-.dat'
uopath = unicode(opath , "utf8")

#infilename = unicode(ipathname , "utf8")
input_file = open(uipath, 'rb')
#outfilename = unicode(opathname , "utf8")
output_file = open(uopath, 'wb')
data = input_file.read(2048)##读取前8个字节
for ch in data:
    print ch
    new_ch = chr(ord(ch) ^ ord(u'\x38'))
    output_file.write(new_ch)
    
##print 'close finally'
input_file.close()
output_file.close()
