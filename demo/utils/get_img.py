#-*- coding: utf-8 -*-

import os
import uuid
import urllib2
import cookielib
import requests
import re
import urllib

from demo.models.ebookmodel import *


img_path="/home/xinghang/spider/"

def get_img_extend_name(img_url):
    img_url = img_url.strip()
    extend_name = '.' + img_url.split('.')[-1]
    return extend_name

books_info = ebookModel.select()

for book_info in books_info:

    try:
        img_url = book_info.img_url
        img_name = book_info.isbn13

        print img_url, img_name

        extend_name = get_img_extend_name(img_url)
        r = requests.get(img_url,stream=True)
        with open(img_path+img_name+extend_name, 'wb') as fd:
            for chunk in r.iter_content():
                fd.write(chunk)
    except:
        pass
