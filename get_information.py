__author__ = 'Moming'

import urllib
from BeautifulSoup import *
import re
import requests



for i in range(10):
    url = 'https://movie.douban.com/top250?start=0' + str(i * 25) + '&filter='
    html = urllib.urlopen(url).read()
    soup = BeautifulSoup(html)
