import socket
from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE

selector = DefaultSelector()
urls_todo = set(['/{}'.format(num) for num in range(10)])
stopped = False

class Future:
    def __init__(self):
        self.result = None
        self._callback = []

    def add_done_callback(self, fn):
        self._callback.append(fn)

    def set_result(self, result):
        self.result = result
        for fn in self._callback:
            fn(self)
class Crawler:
    def __init__(self, url):
        self.url = url
        self.response = b''

    def fetch(self):
        sock = socket.socket()
        sock.setblocking(False)
        try:
            sock.connect(('baidu.com', 80))
        except BlockingIOError:
            pass

        f = Future()
        def on_connected():
            f.set_result(None)

        selector.register(sock.fileno(), EVENT_WRITE, on_connected)
        yield f
        selector.unregister(sock.fileno())
        get = "GET / HTTP/1.0\r\nHOST: baidu.com\r\n\r\n"
        sock.send(get.encode('ascii'))

        global stopped
        while True:
            f = Future()

            def on_recieveable():
                f.set_result(sock.recv(4096))

            selector.register(sock.fileno(), EVENT_READ, on_recieveable)
            chunk = yield f
            selector.unregister(sock.fileno())
            if chunk:
                self.response += chunk
                chunk = yield f
            else:
                urls_todo.remove(self.url)
                if not urls_todo:
                    stopped = True
                break
class Task:
    def __init__(self, coro):
        self.coro = coro
        f = Future()
        f.set_result(None)
        self.step(f)
    def step(self, future):
        try:
            next_future = self.coro.send(future.result)
        except StopIteration:
            return
        next_future.add_done_callback(self.step)

def loop():
    while not stopped:
        events = selector.select()
        for event_key, event_mask in events:
            callback = event_key.data
            callback()

# import socket
# from selectors import DefaultSelector, EVENT_READ, EVENT_WRITE
#
#
# selector = DefaultSelector()
# stopped = False
# urls_todo = set(['/{}'.format(num) for num in range(10)])
#
# class Future:
#     def __init__(self):
#         self.result = None
#         self._callbacks = []
#
#     def add_done_callback(self,fn):
#         self._callbacks.append(fn)
#
#     def set_result(self, result):
#         self.result = result
#         for fn in self._callbacks:
#             fn(self)
#
# class Crawler:
#     def __init__(self, url):
#         self.url = url
#         self.response = b''
#
#     def fetch(self):
#         sock = socket.socket()
#         sock.setblocking(False)
#         try:
#             sock.connect(('baidu.com', 80))
#         except BlockingIOError:
#             pass
#         f = Future()
#         def on_connected():
#             f.set_result(None)
#
#         selector.register(sock.fileno(), EVENT_WRITE, on_connected)
#         yield f
#         selector.unregister(sock.fileno())
#
#         get = 'GET {0} HTTP/1.0\r\nHOST: baidu.com\r\n\r\n'.format(self.url)
#         sock.send(get.encode('ascii'))
#
#         global stopped
#         while True:
#             f = Future()
#             def on_recieved():
#                 f.set_result(sock.recv(4096))
#             selector.register(sock.fileno(), EVENT_READ, on_recieved)
#             chunk = yield f
#             selector.unregister(sock.fileno())
#             if chunk:
#                 self.response += chunk
#             else:
#                 urls_todo.remove(self.url)
#                 if not urls_todo:
#                     stopped = True
#                 break
#
# class Task():
#     def __init__(self, coro):
#         self.coro = coro
#         f = Future()
#         f.set_result(None)
#         self.step(f)
#
#     def step(self, future):
#         try:
#             next_future = self.coro.send(future.result)
#         except StopIteration:
#             return
#         next_future.add_done_callback(self.step)
#
# def loop():
#     while not stopped:
#         events = selector.select()
#         for event_key, event_mast in events:
#             callback = event_key.data
#             callback()
#
if __name__ == '__main__':
    import time
    start_CPU = time.clock()
    for url in urls_todo:
        crawler = Crawler(url)
        Task(crawler.fetch())
    loop()
    end_CPU = time.clock()
    print("Method 1: %f CPU seconds" % (end_CPU - start_CPU))
