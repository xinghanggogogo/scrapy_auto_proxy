# -*- coding: utf-8 -*-
__author__ = 'xinghang'

import scrapy

class tvshowItem(scrapy.Item):

    show_img = scrapy.Field()
    link = scrapy.Field()
    video_link = scrapy.Field()
    title = scrapy.Field()
    anchor = scrapy.Field()
    category = scrapy.Field()
    head_img = scrapy.Field()
    num = scrapy.Field()
    room_id = scrapy.Field()
    source = scrapy.Field()

    md5 = scrapy.Field()
    create_time = scrapy.Field()
    update_time = scrapy.Field()
