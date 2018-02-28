import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

seletor = DefaultSelector()
stopped = False
urls_todo = set(['/{}'.format(num) for num in range(10)])

class Future:
    def __init__(self):
        self.result = None
        self._callback = []
    def add_done_callback(self, fn):
        self._callback.append(fn)
    def set_result(self, result):
        self.result = result
        print('------------------')
        for fn in self._callback:
            print(fn, self)
            fn(self)

    def __iter__(self):
        yield self
        return self.result

def connect(sock, address):
    f = Future()
    # sock = socket.socket()
    sock.setblocking(False)
    try:
        sock.connect(address)
    except BlockingIOError:
        pass
    def on_connect():
        print('connect')
        f.set_result(None)
    seletor.register(sock.fileno(), EVENT_WRITE, on_connect)
    yield from f
    seletor.unregister(sock.fileno())

def read_one(sock):
    f = Future()
    def on_readable():
        res = sock.recv(2048)
        f.set_result(res)
        # print(res)
    seletor.register(sock.fileno(), EVENT_READ, on_readable)
    chunk = yield from f
    seletor.unregister(sock.fileno())
    return chunk
def read_all(sock):
    response = []
    while True:
        chunk = yield from read_one(sock)
        if chunk:
            response.append(chunk)
        else:
            break
    return b''.join(response)

class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''
    def fetch(self):
        # f = Future()
        global stopped
        sock = socket.socket()
        # print('1---'+self.url)
        yield from connect(sock, ('baidu.com', 80))
        get = 'GET / HTTP/1.0\r\nHOST: baidu.com\r\n\r\n'
        sock.send(get.encode('ascii'))
        # print('2---' + self.url)
        self.response = yield from read_all(sock)
        # print(self.url, self.response)
        urls_todo.remove(self.url)
        if not urls_todo:
            stopped = True
class Task:
    def __init__(self, coro, url):
        self.url = url
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)
    def step(self, future):
        print(self.url)
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)

def loop():
    while not stopped:
        events = seletor.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()

if __name__ == '__main__':
    import time
    start_CPU = time.clock()
    for url in urls_todo:
        crawler = Crawler(url)
        Task(crawler.fetch(), url)
    print('############################')
    loop()
    end_CPU = time.clock()
    print("Method 1: %f CPU seconds" % (end_CPU - start_CPU))

# class Future:
#     def __init__(self):
#         self.result = None
#         self._callback = []
#     def add_done_callback(self, fn):
#         self._callback.append(fn)
#     def set_result(self, result):
#         self.result = result
#         for fn in self._callback:
#             fn(self)
#     def __iter__(self):
#         yield self
#         return self.result
#
# def connect(sock, address):
#     f = Future()
#     sock.setblocking(False)
#     try:
#         sock.connect(address)
#     except BlockingIOError:
#         pass
#     def on_connected():
#         f.set_result(None)
#     seletor.register(sock.fileno(), EVENT_WRITE, on_connected)
#     yield from f
#     seletor.unregister(sock.fileno())
# def read(sock):
#     f = Future()
#     def on_readable():
#         f.set_result(sock.recv(4096))
#     seletor.register(sock.fileno(), EVENT_READ, on_readable)
#     yield from f
#     seletor.unregister(sock.fileno())
# def readall(sock):
#     response = []
#     chunk = yield from read(sock)
#     while chunk:
#         response += chunk
#         chunk = yield from read(sock)
#     return b''.join(response)
#
# class Crawler:
#     def __init__(self, url):
#         self.url = url
#         self.response = b''
#     def fetch(self):
#         global stopped
#         sock = socket.socket()
#         # sock.setblocking(False)
#         yield from connect(sock, ('baidu.com', 80))
#         get = 'GET {0} HTTP/1.0\r\nHOST: baidu.com\r\n\r\n'.format(self.url)
#         sock.send(get.encode('ascii'))
#         self.response += yield from readall(sock)
#         urls_todo.remove(self.url)
#         if not urls_todo:
#             stopped = True
#
# class Task:
#     def __init__(self, coro):
#         self.coro = coro
#         f = Future()
#         f.set_result(None)
#         self.step(f)
#     def step(self, future):
#         try:
#             next_future = self.coro.send(future.result)
#         except StopIteration:
#             return
#         next_future.add_done_callback(self.step)
#
# def loop():
#     while not stopped:
#         events = seletor.select()
#         for event_key, event_mask in events:
#             callback = event_key.data
#             callback()
#
# def main():
#     import time
#     start_CPU = time.clock()
#     for url in urls_todo:
#         crawler = Crawler(url)
#         Task(crawler.fetch())
#     loop()
#     end_CPU = time.clock()
#     print("Method 1: %f CPU seconds" % (end_CPU - start_CPU))
#
# main()
