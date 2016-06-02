__author__ = 'Moming'

import urllib
from bs4 import BeautifulSoup as BS
import re
import requests

class Movie(object):
    __title = []
    __url = ''
    __img = ''
    __score = 0
    __director = []
    __starring = []
    __reviews = 0
    __quote = ''
    __label = []
    __year = 1970
    __nation = ''
    
    def __init__(self, Title, Url, Img, Score, Director, Starring, Reviews, Quote, Label):
        self.__title = Title
        self.__url = Url # extract
        self.__img = Img # download
        self.__score = Score
        self.__director = Director
        self.__starring = Starring
        self.__reviews = Reviews
        self.__quote = Quote
        self.__label = Label # year nation

    def get_title(self):
        return self.__title



for i in range(10):
    url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
    html = urllib.urlopen(url).read()
    soup = BS(html)
    movie_divs = soup.findAll('div', {"class": "item"})
    for movie_div in movie_divs:
        img = movie_div.img.attrs['src']

        hd = movie_div.findAll('div', {'class': 'hd'})[0]
        url = hd.a.attrs['href']

        title = []
        main_title = hd.findAll('span', {'class': 'title'})
        for ht in main_title:
            title.append(ht.string.replace(u'\xa0/\xa0', ''))

        other_title = hd.findAll('span', {'class': 'other'})
        title.extend(other_title[0].string.replace(u'\xa0/\xa0', '').split('  /  '))

        bd = movie_div.findAll('div', {'class': 'bd'})[0]
        info = bd.findAll('p', {'class': ''})[0].strings
        flag = True
        while True:
            try:
                cmd = info.next().replace(u'\xa0', '\t').strip()
                if flag:
                    director = cmd.split('\t')[0]
                    starring = cmd.split('\t')[-1]
                    flag = False
                else:
                    label = [x.replace(u'\t', '') for x in cmd.split('/')]
            except StopIteration:
                break

        

