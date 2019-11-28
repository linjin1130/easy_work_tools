import struct
import time

from tornado import ioloop, gen, iostream
from tornado.tcpclient import TCPClient


class TestTcpclient(object):
    """docstring for TestTcpClient"""
    def __init__(self, ip = '127.0.0.1',port = 80):
        self.ip = ip
        self.port = port

    # @gen.coroutine
    # def start(self):
    #     self.stream = yield TCPClient().connect(self.host, self.port)
    #     self.stream.write('hello')
    #     rec=yield self.stream.read_until('/n')
    #     print 'recive from the server',rec

    @gen.coroutine
    def Trans(self):
        stream = yield TCPClient().connect(self.ip, self.port)
        print('connected')
        try:
            while True:
                cmd = 0x05
                ctrl = 0x18
                data0 = 10
                data1 = 1000 << 12
                packedCtrl = struct.pack("l", ctrl)
                unpackedCtrl = struct.unpack('4b', packedCtrl)
                packet = struct.pack("4bLL", cmd, unpackedCtrl[0], unpackedCtrl[1], unpackedCtrl[2], data0, data1)
                yield stream.write(packet )
                # back = yield stream.read_bytes(12, partial=True)
                # print(self.ip, back)
                time.sleep(1)
        except iostream.StreamClosedError:
            print('exception')
            pass

if __name__ == '__main__':
    ip1 = '192.168.1.122'
    # ip1 = '10.0.5.188'
    # ip2 = '10.0.5.194'
    tcp_client1 = TestTcpclient(ip1, port=45000)
    # tcp_client2 = TestTcpclient(ip2)

    # tcp_client2 = TestTcpclient('host', 'port')
    # tcp_client2.start()

    ioloop.IOLoop.current().run_sync(tcp_client1.Trans)
    # ioloop.IOLoop.current().run_sync(tcp_client2.Trans)
    print('hello')
