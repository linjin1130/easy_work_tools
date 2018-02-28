import socket
import time


def blocking_way():
    sock = socket.socket()
    sock.connect(('example.com', 80))
    request = 'GET / HTTP/1.0\r\nHost: example.com\r\n\r\n'
    sock.send(request.encode('ascii'))
    response = b''
    chunk = sock.recv(4096)
    while chunk:
        response += chunk
        chunk = sock.recv(4096)
    return response


def sync_way():
    res = []
    for i in range(10):
        print(i)
        res.append(blocking_way())
    return len(res)


start_CPU = time.clock()
sync_way()
end_CPU = time.clock()
print("Method 1: %f CPU seconds" % (end_CPU - start_CPU))
# t = timeit.timeit('sync_way()', 'from __main__ import sync_way', number=2)
# print(t)
