import socket
from concurrent import futures
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

def process_way():
    workers = 10
    with futures.ProcessPoolExecutor(workers) as execuator:
        futs = {execuator.submit(blocking_way) for i in range(workers)}
    return len([fut.result() for fut in futs])

start_CPU = time.clock()
process_way()
end_CPU = time.clock()