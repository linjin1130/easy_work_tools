import socket
from concurrent import futures

def blocking_way():
    sock = socket.socket()
    sock.connect(('baidu.com',80))
    get = 'GET / HTTP/1.0\r\nHOST: baidu.com\r\n\r\n'
    sock.send(get.encode('ascii'))
    response = b''
    trunk = sock.recv(4096)
    while trunk:
        response += trunk
        trunk = sock.recv(4096)
    return response

def multi_thread_way():
    workers= 10

    with  futures.ThreadPoolExecutor(workers) as executor:
        res = {executor.submit(blocking_way) for i in range(10)}
    return (len(result) for result in res)


# im
#