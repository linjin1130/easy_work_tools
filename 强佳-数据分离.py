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
inpath = r'D:/Work/20160922数据'
uipath = unicode(inpath , "utf8")
opath = r'D:/out'
uopath = unicode(opath , "utf8")
ologpath = r'D:/out/log.csv'
uologpath = unicode(opath , "utf8")
dataseq = 152;    
dataseg = 49448;
##log_file = open('D:/out/log.csv', 'w')
##log_file.write("文件,段号,序号")
for(dirname, dirshere, fileshere) in os.walk(uipath):
    ##print 'cycle'
    ##print '输入路径：',dirname
    for filename in fileshere:
        ipathname = os.path.join(dirname, filename)
        opathname = os.path.join(dirname, "out")
        ##os.makedirs(opathname)
        opathname = os.path.join(uopath, filename)
        filename1 = filename+"00"
        opathname1 = os.path.join(uopath, filename1)
        
        ##print '输入路径：',ipathname
        ##print '输出路径: ', opathname
        if filename.endswith(".dat"):
            ##log_file.write("%s,%d,%d", filename, dataseg, dataseq)
            
            #infilename = unicode(ipathname , "utf8")
            input_file = open(ipathname, 'rb')
            #outfilename = unicode(opathname , "utf8")
            output_file = open(opathname, 'wb')
            output_file1 = open(opathname1, 'wb')
            while 1:
                format = '>19s4081s'##设置头部输入输出格式
                data = input_file.read(4100)##读取前8个字节
                if( len(data) < 4100):
                    break
                values = struct.unpack(format, data)
                ##output_file.write(values[0])
                if(values[0].endswith('\x46\x46')):
                    ##dataseg += 1
                    ##values[1] = str(dataseg)
                    #print values[0]
                    output_file.write(data)
                        ##print '空'
                else:
                    if(values[0].endswith('\x43\x43')):
                        output_file1.write(data)
                    
                
            ##print 'close finally'
            input_file.close()
            output_file.close()
            output_file1.close()
            print "finish"
