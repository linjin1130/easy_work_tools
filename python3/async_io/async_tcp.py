from tornado import ioloop, gen, iostream
from tornado.tcpclient import TCPClient

# @gen.coroutine
# def Trans():
#     stream = yield TCPClient().connect('192.168.1.170', 80)
#     try:
#         while True:
#             yield stream.write(u'12345'.encode('utf-8') )
#             back = yield stream.read_bytes(8, partial=True)
#             print(back)
#     except iostream.StreamClosedError:
#         print('exception')
#         pass
#
# if __name__ == '__main__':
#     ioloop.IOLoop.current().run_sync(Trans)

