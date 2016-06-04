#!/usr/bin/python
# -*- coding: UTF-8 -*-
__author__ = 'Moming'

import urllib
from bs4 import BeautifulSoup as BS
import re
import requests
import os
import cPickle

class Movie(object):
    __title = []
    __url = ''
    __img = ''
    __img_path = ''
    __star = 0
    __director = []
    __starring = []
    __reviews = 0
    __quote = ''
    __label = []
    __year = 1970
    __nation = ''

    def __init__(self, Title, Url, Img, Star, Director, Starring, Reviews, Quote, Label):
        self.__title = Title
        self.__url = Url # extract
        self.__img = Img
        self.__img_path = self.__download_img(Img) # download

        self.__star = Star

        directors = re.findall(r': (.+)', Director)[0]
        for d in directors.split('/'):
            self.__director.append(d.strip())

        self.__starring = Starring
        self.__reviews = Reviews
        self.__quote = Quote

        self.__year = int(re.findall(r'(\d{1,8})', Label[0])[0])
        self.__nation = Label[1]
        self.__label = Label[2].split(' ')


    def __download_img(self, url):
        if not os.path.isdir('./images'):
            os.mkdir('./images')

        path = './images/' + url.split('/')[-1]
        if os.path.isfile(path):
            return path

        fw = open(path, 'wb')
        fw.write(requests.get(url).content)
        fw.close()
        return path


    def get_title(self):
        return self.__title

    def get_url(self):
        return self.__url

    def get_star(self):
        return self.__star

    def get_director(self):
        return self.__director

    def get_starring(self):
        return self.__starring

    def get_label(self):
        return self.__label

    def get_year(self):
        return self.__year

    def get_nation(self):
        return self.__nation

    def get_reviews(self):
        return self.__reviews

    def get_quote(self):
        return self.__quote



MovieTable = []

for i in range(10):
    url = 'https://movie.douban.com/top250?start=' + str(i * 25) + '&filter='
    html = urllib.urlopen(url).read()
    soup = BS(html, 'html.parser')
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
        director = ''
        starring = ''
        label = []
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

        star_span = bd.find('span', {'class': 'rating_num'})
        star = float(star_span.string)
        reviews_span = star_span.next_sibling.next_sibling.next_sibling.next_sibling
        reviews = int(re.findall(r'(\d{1,10})', reviews_span.string)[0])

        if bd.find('span', {'class': 'inq'}) == None:
            quote = ''
        else:
            quote = bd.find('span', {'class': 'inq'}).string

        douban_movie = Movie(title, url, img, star, director, starring, reviews, quote, label)

        MovieTable.append(douban_movie)

if not os.path.isdir('./Movies'):
    os.mkdir('./Movies')

store_path = './Movies/movie_table.pkl'
cPickle.dump(MovieTable, open(store_path, 'w'))