import socket
import struct
class network_switch(object):
    """
        网络开关板对象
        实现与网络开关硬件的连接，
        """
    def __init__(self):
        self.port       = 1234
        self.channel_amount = 8
        # Initialize core parameters
        self.sockfd = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sockfd.settimeout(5.0)
        self.soft_version = None

    def connect(self, addr):
        """Connect to Server"""
        #host = '149.199.131.176'
        host = addr
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

    def switch_open(self, channel):
        assert channel in range(1,8)
        cmd = f'L{channel}/r/n'
        self.send_data(bytes(cmd, encoding='utf-8'))

    def switch_close(self, channel):
        assert channel in range(1,8)
        cmd = f'D{channel}/r/n'
        self.send_data(bytes(cmd, encoding='utf-8'))

    def send_data(self, msg):
        """Send data over the socket."""
        totalsent = 0
        while totalsent < len(msg):
            sent = self.sockfd.send(msg)
            if sent == 0:
                raise RuntimeError("Socket connection broken")
            totalsent = totalsent + sent
        self.receive_data()

    def receive_data(self):
        """Read received data from the socket."""
        bytes_recd = 0
        chunk = self.sockfd.recv(1024)
        if chunk == '':
           raise RuntimeError("Socket connection broken")
        print(chunk)
        return chunk
