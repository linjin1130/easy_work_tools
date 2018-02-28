import socket
from selectors import DefaultSelector, EVENT_WRITE, EVENT_READ

selector = DefaultSelector()
urls_todo = set(['/{}'.format(num) for num in range(10)])
stopped = False

class Crawler:
    def __init__(self, url):
        self.url = url
        self.sock = socket.socket()
        self.response = b''
    def fetch(self):
        # sock = socket.socket()
        self.sock.setblocking(False)
        try:
            self.sock.connect(self.url)
        except BlockingIOError:
            pass
        selector.register(self.sock.fileno(), EVENT_WRITE, on_connected)

    def on_connected(self, event_key, event_mask):
        selector.unregister(event_key.fd)
        get = 'GET / HTTP1.0\r\nHOST: baidu.com\r\n\r\n'
        self.sock.send(get.encode('ascii'))
        selector.register(self.sock.fileno(), EVENT_READ, read_response)

    def read_response(self, event_key, event_mask):
        global stopped
        # selector.unregister(event_key.fd)
        response = b''
        chunk = self.sock.recv(4096)
        if chunk:
            self.response += chunk
        else:
            selector.unregister(event_key.fd)
            urls_todo.remove(self.url)
            if not urls_todo:
                stopped = True

def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callable(event_key, event_mask)

if __name__=='__main__':
    for url in urls_todo:
        crawler = Crawler(url)
        crawler.fetch()
    loop()


# import socket
#
# def nonblocking_way(url):
#     sock = socket.socket()
#     sock.setblocking(False)
#
#     try:im
#         sock.connect(url)
#     except BlockingIOError:
#         pass
#
#     get = 'GET / HTTP/1.0\r\nHOST: baidu.com\r\n\r\n'
#     while True:
#         try:
#             sock.send(get.encode('ascii'))
#             break
#         except BlockingIOError:
#             pass
#     response = b''
#     while True:
#         try:
#             trunk = sock.recv(4096)
#             while True:
#                 response += trunk
#                 trunk = sock.recv(4096)
#             break
#         except BlockingIOError:
#             pass
#
#     def sync_way():
#         res = []
#         for item in range(10):
#             res.append(nonblocking_way(url))
#         return len(res)