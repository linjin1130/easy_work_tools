import xml.sax

class MyHandler(xml.sax.ContentHandler):
    def startElement(self, name, attrs):
        print('start element'+name)
    def endElement(self, name):
        print('end element')
    def characters(self, content):
        print('characters'+repr(content)[:40])

xml.sax.parse('allroutes', MyHandler())