def countdown(n):
    print('countdown from %d' % (n))
    while n:
        yield n
        n -= 1

# x = countdown(10)
# print(x)
# print(x.__next__())
# print(x.__next__())

import time
def follw(thefile):
    thefile.seek(0,2) #go to the end of the file
    while True:
        line = thefile.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line

# def grep(patten, lines):
#     for line in lines:
#         if patten in line:
#             yield line
#
# logfile = open('access-log')
# lines = follw(logfile)
# filter = grep('python', lines)
#
# for line in filter:
#     print(line)

def grep(patten):
    print('filter for {0}'.format(patten))
    while True:
        line = (yield)
        if patten in line:
            print(line)

# g = grep('python')
# g.__next__()
# g.send('haha')
# g.send('hehe')
# g.send('python for you')
# g.close()

def coroutine(func):
    def grep()