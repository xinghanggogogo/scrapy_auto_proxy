# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import scrapy


class proxyItem(scrapy.Item):

    ip = scrapy.Field()
    port = scrapy.Field()

