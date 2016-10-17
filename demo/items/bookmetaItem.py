# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import scrapy


class bookmetaItem(scrapy.Item):

    name = scrapy.Field()
    img_url = scrapy.Field()
    author = scrapy.Field()
    total_pages = scrapy.Field()
    key_words = scrapy.Field()
    category = scrapy.Field()
    introduction = scrapy.Field()
    comments = scrapy.Field()
    publisher = scrapy.Field()
    publication_date = scrapy.Field()
    publication_city = scrapy.Field()
    hot_level = scrapy.Field()
    isbn10 = scrapy.Field()
    isbn13 = scrapy.Field()

    md5 = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()

class bookcommentItem(scrapy.Item):

    book_name = scrapy.Field()
    title = scrapy.Field()
    time = scrapy.Field()
    content= scrapy.Field()
    isbn13 = scrapy.Field()

    md5 = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()