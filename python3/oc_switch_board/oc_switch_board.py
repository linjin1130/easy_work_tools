import math
import socket
import struct
from itertools import repeat, chain
# import numpy as np

class oc_switch_board(object):
    def __init__(self):
        self.port       = 1234
        self.ip       = '127.0.0.1'
        self.channel_amount = 8
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockfd.settimeout(5.0)

    def connect(self):
        """Connect to Server"""
        #host = '149.199.131.176'
        host = self.ip
        print ('Host name is: {}'.format(host))
        try:
            self.sockfd.connect((host, self.port))
            print ('connected')
            return 1
        except socket.error as msg:
            self.sockfd.close()
            self.sockfd = None
        if self.sockfd is None:
            print ('ERROR:Could not open socket')
            return -1

    def disconnect(self):
        """Close the connection to the server."""
        if self.sockfd is not None:
            print ('Closing socket')
            self.sockfd.close()

    def send_data(self, msg):
        """Send data over the socket."""
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sockfd.send(msg)
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent = totalsent + sent

    def receive_data(self):
        """Read received data from the socket."""
        chunks = []
        bytes_recd = 0
        while bytes_recd < 8:
            #I'm reading my data in byte chunks
            chunk = self.sockfd.recv(min(8 - bytes_recd, 4))
            if chunk == '':
               raise RuntimeError("Socket connection broken")
            chunks.append(chunk)
            bytes_recd = bytes_recd + len(chunk)
        stat_tuple = struct.unpack('L', chunks[0])
        data_tuple = struct.unpack('L', chunks[1])
        stat = stat_tuple[0]
        data = data_tuple[0]
        return stat, chunks[1]

    def Open(self, Channel='A'):
        msg = (u'L'+str(Channel)+'\r\n').encode(encoding='utf-8')
        self.send_data(msg)
        return

    def Close(self, Channel='A'):
        msg = (u'D'+str(Channel)+'\r\n').encode(encoding='utf-8')
        self.send_data(msg)
        return