import time
def follow(thefile, target):
    thefile.seek(0, 2)
    while True:
        item = thefile.readline()
        if item:
            target.send(item)
        else:
            time.sleep(0.1)

def coroutine(func):
    def start(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr
    return start

@coroutine
def filter(pattern, target):
    while True:
        line = yield
        if pattern in line:
            target.send(line)

@coroutine
def printer():
    while True:
        item = yield
        print(item)

@coroutine
def broadcast(targets):
    while True:
        item = yield
        for target in targets:
            target.send(item)

class Grep:
    def __init__(self, patten, target):
        self.patten = patten
        self.target = target
    def send(self, line):
        if self.patten in line:
            self.target.send(line)



f = open('access-log')
follow(f, filter('ico',printer()))
# follow(f, broadcast([printer(), printer()]))