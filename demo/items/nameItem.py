# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import scrapy


class nameItem(scrapy.Item):

    gender = scrapy.Field()
    ename = scrapy.Field()
    sounce = scrapy.Field()
    cname = scrapy.Field()
    source = scrapy.Field()
    charactors = scrapy.Field()
    hot_level = scrapy.Field()
    detail_link = scrapy.Field()
    detail = scrapy.Field()
    masters = scrapy.Field()

    md5 = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
