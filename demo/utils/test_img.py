#-*- coding: utf-8 -*-

'''
验证图片可用
'''

import requests
import time

from demo.models.ebookmodel import *

books_info = ebookModel.select()

for book_info in books_info:
    try:
        img_url = book_info.img_url
        time.sleep(1)
        res = requests.get(img_url, stream=True)
        if res.content[0:3] == 'GIF':
            peewee_sql = ebookModel.update(img_url='').where(ebookModel.isbn10 == book_info.isbn10)
            peewee_sql.execute()
    except:
        pass


# for book_info in books_info:
#     try:
#         isbn10 = book_info.isbn10
#         img_url = 'http://ec1.images-amazon.com/images/P/%s.01._SX220_SCLZZZZZZZ_.jpg' % isbn10
#         query_sql = book_info.update(img_url=img_url).where(ebookModel.isbn10 == isbn10)
#         query_sql.execute()
#     except:
#         pass