def fact(n):
    '''
    >>> fact(0)
    Traceback (most recent call last):
        ...
    ValueError
    >>> fact(1)
    1
    >>> fact(20)
    2432902008176640000
    '''
    if n < 1:
        raise ValueError()
    if n == 1:
        return 1
    return n * fact(n-1)

if __name__ == '__name__':
    import doctest
    doctest.testmod()

# # from BeautifulSoup import BeautifulSoup          # For processing HTML
# # from BeautifulSoup import BeautifulStoneSoup     # For processing XML
# # import BeautifulSoup                             # To get everything
# html_doc = """
# <html><head><title>The Dormouse's story</title></head>
# <body>
# <p class="title"><b>The Dormouse's story</b></p>
#
# <p class="story">Once upon a time there were three little sisters; and their names were
# <a href="http://example.com/elsie" class="sister" id="link1">Elsie</a>,
# <a href="http://example.com/lacie" class="sister" id="link2">Lacie</a> and
# <a href="http://example.com/tillie" class="sister" id="link3">Tillie</a>;
# and they lived at the bottom of a well.</p>
#
# <p class="story">...</p>
# """
#
# from bs4 import BeautifulSoup
# soup = BeautifulSoup(html_doc, 'html.parser')
#
# # print(soup.prettify())
# print(soup.title)
# print(soup.title.name)
# print(soup.title.string)
# print(soup.title.parent.name)
# print(soup.p)
# print(soup.p['class'])
# print(soup.a)
# print(soup.a['class'])
# print(soup.find_all('a'))
# print(soup.find_all(id='link3'))
#
# for a in soup.find_all('a'):
#     print(a['href'], a['id'])
#
# print(soup.get_text())