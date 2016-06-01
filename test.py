import urllib
from bs4 import BeautifulSoup as BS

url = 'https://movie.douban.com/top250?start=0&filter='
html = urllib.urlopen(url).read()
soup = BS(html)
mydivs = soup.findAll('div', {"class": "item"})