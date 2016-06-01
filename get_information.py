__author__ = 'Moming'

import urllib
from bs4 import BeautifulSoup as BS
import re
import requests



for i in range(10):
    url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
    html = urllib.urlopen(url).read()
    soup = BS(html)
    mydivs = soup.findAll('div', {"class": "item"})