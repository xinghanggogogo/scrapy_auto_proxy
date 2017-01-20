# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import scrapy


class oneItem(scrapy.Item):

    img_url = scrapy.Field()
    img_author = scrapy.Field()
    text = scrapy.Field()

    md5 = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()