import xml.sax

class EventHandler(xml.sax.ContentHandler):
    def __init__(self, target):
        self.target = target
    def startElement(self, name, attrs):
        self.target.send(('start', (name, attrs._attrs)))
    def endElement(self, name):
        self.target.send(('end', name))
    def characters(self, content):
        self.target.send(('text', content))

def coroutines(func):
    def wrapper(*args, **kwargs):
        cr = func(*args, **kwargs)
        cr.send(None)
        return cr
    return wrapper
@coroutines
def buses_to_dicts(target):
    while True:
        event, value = yield
        if event == 'start' and value[0] == 'bus':
            # print(event, value)
            busdic = {}
            fragments = []
            while True:
                event, value = (yield)
                # print(event, value)
                if event == 'start': fragments = []
                elif event == 'text': fragments.append(value)
                elif event == 'end':
                    if value != "bus":
                        # print(value)
                        busdic[value] = "".join(fragments)
                    else:
                        # print("haha")
                        # print(busdic)
                        target.send(busdic)
                        break

@coroutines
def filter_on_field(fieldname, value, target):
    while True:
        d = yield
        if d.get(fieldname) == value:
            target.send(d)
@coroutines
def printer():
    while True:
        item = yield
        print(item)

@coroutines
def bus_locations():
    while True:
        bus = yield
        print("%(route)s,%(id)s,\"%(direction)s\"," "%(latitude)s,%(longitude)s" % bus)

xml.sax.parse('allroutes.xml', EventHandler(
    buses_to_dicts(
        filter_on_field('route', '22',
                        filter_on_field('direction', 'North Bound',
                                        bus_locations()))
    )
))

# from xml.etree.cElementTree import iterparse
#
# for event, elem in iterparse('allroutes.xml', ('start', 'end')):
#     if event == 'start' and elem.tag == 'buses':
#         buses = elem
#     elif event == 'end' and elem.tag == 'bus':
#         busdict = dict((child.tag, child.text) for child in elem)
#         if (busdict['route'] == '22' and busdict['direction'] == 'North Bound'):            print
#         "%(id)s,%(route)s,\"%(direction)s\"," "%(latitude)s,%(longitude)s" % busdict
#         buses.remove(elem)