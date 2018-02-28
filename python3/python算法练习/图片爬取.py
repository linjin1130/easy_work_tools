import os
import uuid

import requests
from bs4 import BeautifulSoup

url = 'http://tieba.baidu.com/p/2166231880'
html = requests.get(url)
soup = BeautifulSoup(html.text, 'html.parser')
img_urls = soup.findAll('img', bdwater='杉本有美吧,1280,860')
count = 1
for img_url in img_urls:
    img_src = img_url['src']
    # print(img_src)
    # os.path.split(img_src)[1]
    img = requests.get(img_src)
    with open(('%s.jpg' % count), 'wb') as f:
        f.write(img.content)
    count += 1

def get_file_extension(file):
    return os.path.splitext(file)[-1]

def mkdir(path):
    path=path.strip()
    path=path.rstrip('\\')
    if not os.path.exists(path):
        os.makedirs(path)
    return path

def unique_id():
    return str(uuid.uuid1())

